"""
Django views for lab report image processing and upload handling.
"""

import json
import base64
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import tempfile
from PIL import Image
import io

# Import our lab report processor
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Agent', 'healthguard', 'src', 'healthguard', 'tools'))

try:
    from lab_report_processor import LabReportImageProcessor, process_base64_image
except ImportError:
    # Fallback if import fails
    LabReportImageProcessor = None
    process_base64_image = None

from .services import HealthDataService


@csrf_exempt
@require_http_methods(["POST"])
def upload_lab_report_image(request):
    """
    API endpoint to upload and process lab report images.
    Accepts both file uploads and base64 encoded images.
    """
    try:
        user_id = request.POST.get('user_id', 1)
        
        # Check if we have the processor available
        if not LabReportImageProcessor:
            return JsonResponse({
                'success': False,
                'error': 'Lab report processor not available. Please install required dependencies: pip install opencv-python pytesseract pillow'
            }, status=500)
        
        processed_data = None
        
        # Handle file upload
        if 'lab_report_image' in request.FILES:
            uploaded_file = request.FILES['lab_report_image']
            
            # Validate file type
            if not uploaded_file.content_type.startswith('image/'):
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid file type. Please upload an image file.'
                }, status=400)
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name
            
            try:
                # Process the image
                processor = LabReportImageProcessor()
                processed_data = processor.process_lab_report_image(temp_path)
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        # Handle base64 encoded image
        elif 'image_base64' in request.POST:
            base64_string = request.POST['image_base64']
            
            # Remove data URL prefix if present
            if base64_string.startswith('data:image'):
                base64_string = base64_string.split(',')[1]
            
            processed_data = process_base64_image(base64_string)
        
        # Handle JSON body with base64 image
        else:
            try:
                data = json.loads(request.body)
                if 'image_base64' in data:
                    base64_string = data['image_base64']
                    user_id = data.get('user_id', user_id)
                    
                    # Remove data URL prefix if present
                    if base64_string.startswith('data:image'):
                        base64_string = base64_string.split(',')[1]
                    
                    processed_data = process_base64_image(base64_string)
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'No image data provided. Use lab_report_image file upload or image_base64 parameter.'
                    }, status=400)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON data.'
                }, status=400)
        
        if not processed_data:
            return JsonResponse({
                'success': False,
                'error': 'No image data to process.'
            }, status=400)
        
        # Check if processing was successful
        if processed_data.get('error'):
            return JsonResponse({
                'success': False,
                'error': processed_data.get('message', 'Unknown processing error')
            }, status=500)
        
        # Save to database if processing was successful
        try:
            lab_data = {
                'lab_test_name': processed_data['lab_test_name'],
                'lab_date_conducted': processed_data['lab_date_conducted'],
                'lab_results': processed_data['lab_results'],
                'lab_normal_ranges': processed_data['lab_normal_ranges'],
                'interpretation_summary': processed_data['interpretation_summary'],
                'interpretation_abnormalities': processed_data['interpretation_abnormalities'],
                'recommendation_date': processed_data['recommendation_date'],
                'recommendation_action': processed_data['recommendation_action'],
            }
            
            # Convert date strings to date objects
            from datetime import datetime
            lab_data['lab_date_conducted'] = datetime.strptime(lab_data['lab_date_conducted'], '%Y-%m-%d').date()
            lab_data['recommendation_date'] = datetime.strptime(lab_data['recommendation_date'], '%Y-%m-%d').date()
            
            # Save to database using existing service
            from ..models import LabResult, User
            from django.shortcuts import get_object_or_404
            
            user = get_object_or_404(User, id=user_id)
            lab_result = LabResult.objects.create(
                user=user,
                lab_test_name=lab_data['lab_test_name'],
                lab_date_conducted=lab_data['lab_date_conducted'],
                lab_results=lab_data['lab_results'],
                lab_normal_ranges=lab_data['lab_normal_ranges'],
                interpretation_summary=lab_data['interpretation_summary'],
                interpretation_abnormalities=lab_data['interpretation_abnormalities'],
                recommendation_date=lab_data['recommendation_date'],
                recommendation_action=lab_data['recommendation_action']
            )
            
            processed_data['database_saved'] = True
            processed_data['lab_result_id'] = lab_result.id
            
        except Exception as db_error:
            # Processing succeeded but database save failed
            processed_data['database_saved'] = False
            processed_data['database_error'] = str(db_error)
        
        return JsonResponse({
            'success': True,
            'message': 'Lab report processed successfully',
            'data': processed_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def analyze_lab_text(request):
    """
    API endpoint to analyze lab report text (for cases where text is already extracted).
    """
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id', 1)
        lab_text = data.get('lab_text', '')
        
        if not lab_text:
            return JsonResponse({
                'success': False,
                'error': 'No lab text provided for analysis.'
            }, status=400)
        
        if not LabReportImageProcessor:
            return JsonResponse({
                'success': False,
                'error': 'Lab report processor not available.'
            }, status=500)
        
        # Create processor and analyze text
        processor = LabReportImageProcessor()
        
        # Parse the text
        parsed_data = processor.parse_lab_parameters(lab_text)
        
        # Analyze results
        analysis = processor.analyze_results(parsed_data)
        
        # Combine results
        result = {
            'lab_test_name': parsed_data['test_metadata'].get('report_type', 'Lab Report'),
            'lab_date_conducted': parsed_data['patient_info'].get('date', ''),
            'lab_results': {param: data['value'] for param, data in parsed_data['lab_results'].items()},
            'lab_normal_ranges': parsed_data['lab_normal_ranges'],
            'patient_info': parsed_data['patient_info'],
            'interpretation_summary': analysis['interpretation_summary'],
            'interpretation_abnormalities': analysis['interpretation_abnormalities'],
            'recommendation_action': '; '.join(analysis.get('recommendations', [])),
            'severity_level': analysis['severity_level'],
            'parameters_extracted': len(parsed_data['lab_results']),
            'processing_timestamp': processor.datetime.now().isoformat()
        }
        
        return JsonResponse({
            'success': True,
            'message': f'Lab text analyzed successfully. {len(parsed_data["lab_results"])} parameters extracted.',
            'data': result
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Analysis error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_lab_report_status(request):
    """
    API endpoint to check the status of lab report processing capabilities.
    """
    try:
        # Check if required dependencies are available
        dependencies_status = {
            'opencv': False,
            'pytesseract': False,
            'pillow': False,
            'processor_available': False
        }
        
        try:
            import cv2
            dependencies_status['opencv'] = True
        except ImportError:
            pass
        
        try:
            import pytesseract
            dependencies_status['pytesseract'] = True
        except ImportError:
            pass
        
        try:
            from PIL import Image
            dependencies_status['pillow'] = True
        except ImportError:
            pass
        
        dependencies_status['processor_available'] = LabReportImageProcessor is not None
        
        # Check Tesseract installation
        tesseract_available = False
        if dependencies_status['pytesseract']:
            try:
                import pytesseract
                pytesseract.get_tesseract_version()
                tesseract_available = True
            except Exception:
                pass
        
        dependencies_status['tesseract_executable'] = tesseract_available
        
        # Overall status
        all_ready = all([
            dependencies_status['opencv'],
            dependencies_status['pytesseract'],
            dependencies_status['pillow'],
            dependencies_status['processor_available'],
            dependencies_status['tesseract_executable']
        ])
        
        installation_commands = []
        if not dependencies_status['opencv']:
            installation_commands.append('pip install opencv-python')
        if not dependencies_status['pytesseract']:
            installation_commands.append('pip install pytesseract')
        if not dependencies_status['pillow']:
            installation_commands.append('pip install pillow')
        if not dependencies_status['tesseract_executable']:
            installation_commands.append('Install Tesseract OCR: https://github.com/tesseract-ocr/tesseract')
        
        return JsonResponse({
            'success': True,
            'ready_for_processing': all_ready,
            'dependencies_status': dependencies_status,
            'installation_commands': installation_commands,
            'supported_formats': ['JPEG', 'PNG', 'TIFF', 'BMP'],
            'supported_methods': ['file_upload', 'base64_encoding'],
            'features': [
                'OCR text extraction',
                'Lab parameter identification',
                'Normal range detection',
                'Abnormality analysis',
                'Clinical recommendations',
                'Database integration'
            ]
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Status check error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def batch_process_lab_reports(request):
    """
    API endpoint to process multiple lab report images in batch.
    """
    try:
        user_id = request.POST.get('user_id', 1)
        
        if not LabReportImageProcessor:
            return JsonResponse({
                'success': False,
                'error': 'Lab report processor not available.'
            }, status=500)
        
        # Get all uploaded files
        uploaded_files = []
        for key in request.FILES:
            if key.startswith('lab_report_'):
                uploaded_files.append(request.FILES[key])
        
        if not uploaded_files:
            return JsonResponse({
                'success': False,
                'error': 'No lab report images provided for batch processing.'
            }, status=400)
        
        results = []
        processor = LabReportImageProcessor()
        
        for idx, uploaded_file in enumerate(uploaded_files):
            try:
                # Validate file type
                if not uploaded_file.content_type.startswith('image/'):
                    results.append({
                        'file_index': idx,
                        'filename': uploaded_file.name,
                        'success': False,
                        'error': 'Invalid file type'
                    })
                    continue
                
                # Save temporarily and process
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                    for chunk in uploaded_file.chunks():
                        temp_file.write(chunk)
                    temp_path = temp_file.name
                
                try:
                    # Process the image
                    processed_data = processor.process_lab_report_image(temp_path)
                    
                    if processed_data.get('error'):
                        results.append({
                            'file_index': idx,
                            'filename': uploaded_file.name,
                            'success': False,
                            'error': processed_data.get('message', 'Processing failed')
                        })
                    else:
                        results.append({
                            'file_index': idx,
                            'filename': uploaded_file.name,
                            'success': True,
                            'data': processed_data,
                            'parameters_extracted': len(processed_data.get('lab_results', {}))
                        })
                
                finally:
                    # Clean up temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
            except Exception as file_error:
                results.append({
                    'file_index': idx,
                    'filename': uploaded_file.name,
                    'success': False,
                    'error': str(file_error)
                })
        
        # Summary
        successful = sum(1 for r in results if r['success'])
        total_parameters = sum(r.get('parameters_extracted', 0) for r in results if r['success'])
        
        return JsonResponse({
            'success': True,
            'message': f'Batch processing completed. {successful}/{len(results)} files processed successfully.',
            'summary': {
                'total_files': len(results),
                'successful': successful,
                'failed': len(results) - successful,
                'total_parameters_extracted': total_parameters
            },
            'results': results
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Batch processing error: {str(e)}'
        }, status=500)