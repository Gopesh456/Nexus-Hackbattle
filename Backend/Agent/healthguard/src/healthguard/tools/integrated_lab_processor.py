"""
Integrated Lab Report Processing Tool for CrewAI Health Agents
Combines image processing, database integration, and AI analysis
"""

import os
import sys
import json
import base64
import tempfile
from typing import Dict, Any, Optional, List
from datetime import datetime

# Add paths for imports
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

try:
    from lab_report_processor import LabReportImageProcessor, process_base64_image
    PROCESSOR_AVAILABLE = True
except ImportError:
    LabReportImageProcessor = None
    process_base64_image = None
    PROCESSOR_AVAILABLE = False

# Try to import Django components for database integration
try:
    import django
    from django.conf import settings
    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False


class IntegratedLabReportTool:
    """
    Comprehensive tool for processing lab reports from images and integrating with health system.
    Designed for use with CrewAI agents and health management systems.
    """
    
    def __init__(self, user_id: int = 1, django_setup: bool = True):
        self.user_id = user_id
        self.processor = None
        self.django_ready = False
        
        # Initialize image processor if available
        if PROCESSOR_AVAILABLE:
            self.processor = LabReportImageProcessor()
        
        # Setup Django if requested and available
        if django_setup and DJANGO_AVAILABLE:
            self._setup_django()
    
    def _setup_django(self):
        """Setup Django environment for database operations."""
        try:
            if not settings.configured:
                # Django settings path should be set in environment
                os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus.settings')
                django.setup()
            self.django_ready = True
        except Exception as e:
            print(f"Django setup failed: {e}")
            self.django_ready = False
    
    def get_processing_status(self) -> Dict[str, Any]:
        """
        Get the current status of processing capabilities.
        
        Returns:
            Status information dictionary
        """
        status = {
            'image_processing_available': PROCESSOR_AVAILABLE,
            'database_integration_available': self.django_ready,
            'supported_formats': ['JPEG', 'PNG', 'TIFF', 'BMP'] if PROCESSOR_AVAILABLE else [],
            'features': []
        }
        
        if PROCESSOR_AVAILABLE:
            status['features'].extend([
                'OCR text extraction',
                'Lab parameter identification',
                'Normal range detection',
                'Abnormality analysis',
                'Clinical recommendations'
            ])
        
        if self.django_ready:
            status['features'].append('Database integration')
        
        return status
    
    def process_lab_image_from_path(self, image_path: str, save_to_db: bool = True) -> Dict[str, Any]:
        """
        Process lab report from image file path.
        
        Args:
            image_path: Path to the lab report image
            save_to_db: Whether to save results to database
            
        Returns:
            Processed lab report data
        """
        if not PROCESSOR_AVAILABLE:
            return {
                'success': False,
                'error': 'Image processing not available. Install required dependencies: pip install opencv-python pytesseract pillow',
                'processing_method': 'image_processing'
            }
        
        if not os.path.exists(image_path):
            return {
                'success': False,
                'error': f'Image file not found: {image_path}',
                'processing_method': 'image_processing'
            }
        
        try:
            # Process the image
            result = self.processor.process_lab_report_image(image_path)
            
            if result.get('error'):
                return {
                    'success': False,
                    'error': result.get('message', 'Image processing failed'),
                    'processing_method': 'image_processing'
                }
            
            # Add metadata
            result['processing_method'] = 'image_processing'
            result['success'] = True
            result['confidence_score'] = self._calculate_confidence_score(result)
            
            # Save to database if requested and available
            if save_to_db and self.django_ready:
                db_result = self._save_to_database(result)
                result.update(db_result)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Processing error: {str(e)}',
                'processing_method': 'image_processing'
            }
    
    def process_lab_image_from_base64(self, base64_string: str, save_to_db: bool = True) -> Dict[str, Any]:
        """
        Process lab report from base64 encoded image.
        
        Args:
            base64_string: Base64 encoded image data
            save_to_db: Whether to save results to database
            
        Returns:
            Processed lab report data
        """
        if not PROCESSOR_AVAILABLE:
            return {
                'success': False,
                'error': 'Image processing not available',
                'processing_method': 'image_processing'
            }
        
        try:
            # Remove data URL prefix if present
            if base64_string.startswith('data:image'):
                base64_string = base64_string.split(',')[1]
            
            # Process the base64 image
            result = process_base64_image(base64_string)
            
            if result.get('error'):
                return {
                    'success': False,
                    'error': result.get('message', 'Image processing failed'),
                    'processing_method': 'image_processing'
                }
            
            # Add metadata
            result['processing_method'] = 'image_processing'
            result['success'] = True
            result['confidence_score'] = self._calculate_confidence_score(result)
            
            # Save to database if requested and available
            if save_to_db and self.django_ready:
                db_result = self._save_to_database(result)
                result.update(db_result)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Processing error: {str(e)}',
                'processing_method': 'image_processing'
            }
    
    def process_lab_text(self, lab_text: str, save_to_db: bool = True) -> Dict[str, Any]:
        """
        Process lab report from pre-extracted text.
        
        Args:
            lab_text: Raw text from lab report
            save_to_db: Whether to save results to database
            
        Returns:
            Processed lab report data
        """
        if not PROCESSOR_AVAILABLE:
            return {
                'success': False,
                'error': 'Text processing not available',
                'processing_method': 'text_analysis'
            }
        
        try:
            # Parse the text
            parsed_data = self.processor.parse_lab_parameters(lab_text)
            
            # Analyze results
            analysis = self.processor.analyze_results(parsed_data)
            
            # Combine results
            result = {
                'success': True,
                'lab_test_name': parsed_data['test_metadata'].get('report_type', 'Lab Report'),
                'lab_date_conducted': parsed_data['patient_info'].get('date', datetime.now().strftime('%Y-%m-%d')),
                'lab_results': {param: data['value'] for param, data in parsed_data['lab_results'].items()},
                'lab_normal_ranges': parsed_data['lab_normal_ranges'],
                'patient_info': parsed_data['patient_info'],
                'interpretation_summary': analysis['interpretation_summary'],
                'interpretation_abnormalities': analysis['interpretation_abnormalities'],
                'recommendation_date': datetime.now().strftime('%Y-%m-%d'),
                'recommendation_action': '; '.join(analysis.get('recommendations', [])),
                'severity_level': analysis['severity_level'],
                'parameters_extracted': len(parsed_data['lab_results']),
                'processing_method': 'text_analysis',
                'confidence_score': self._calculate_confidence_score(parsed_data),
                'extracted_text': lab_text,
                'processing_timestamp': datetime.now().isoformat(),
                'message': f"Lab text analyzed successfully. {len(parsed_data['lab_results'])} parameters extracted and analyzed."
            }
            
            # Save to database if requested and available
            if save_to_db and self.django_ready:
                db_result = self._save_to_database(result)
                result.update(db_result)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Text processing error: {str(e)}',
                'processing_method': 'text_analysis'
            }
    
    def get_existing_lab_data(self, test_name: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Retrieve existing lab data from database.
        
        Args:
            test_name: Optional filter by test name
            limit: Maximum number of results
            
        Returns:
            Existing lab data
        """
        if not self.django_ready:
            return {
                'success': False,
                'error': 'Database not available',
                'data': []
            }
        
        try:
            # Import Django models
            from healthapp.services import HealthDataService
            
            # Get lab results
            lab_results = HealthDataService.get_lab_results(self.user_id, test_name) or []
            
            # Limit results
            lab_results = lab_results[:limit]
            
            return {
                'success': True,
                'data': lab_results,
                'count': len(lab_results),
                'message': f'Retrieved {len(lab_results)} lab result(s) from database.'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Database query error: {str(e)}',
                'data': []
            }
    
    def compare_with_previous_results(self, current_results: Dict[str, Any], 
                                    days_back: int = 90) -> Dict[str, Any]:
        """
        Compare current lab results with previous results.
        
        Args:
            current_results: Current lab results data
            days_back: How many days back to look for comparison
            
        Returns:
            Comparison analysis
        """
        if not self.django_ready:
            return {
                'success': False,
                'error': 'Database not available for comparison',
                'comparison': {}
            }
        
        try:
            # Get previous results
            previous_data = self.get_existing_lab_data(limit=5)
            
            if not previous_data['success'] or not previous_data['data']:
                return {
                    'success': True,
                    'comparison': {
                        'has_previous_data': False,
                        'message': 'No previous lab data available for comparison.'
                    }
                }
            
            # Compare parameters
            current_params = current_results.get('lab_results', {})
            comparison_results = {
                'has_previous_data': True,
                'trends': {},
                'significant_changes': [],
                'stable_parameters': [],
                'new_parameters': []
            }
            
            # Find the most recent previous result with overlapping parameters
            for prev_result in previous_data['data']:
                prev_params = prev_result.get('results', {})
                
                for param, current_value in current_params.items():
                    if param in prev_params:
                        prev_value = prev_params[param]
                        if isinstance(current_value, (int, float)) and isinstance(prev_value, (int, float)):
                            change = current_value - prev_value
                            percent_change = (change / prev_value * 100) if prev_value != 0 else 0
                            
                            comparison_results['trends'][param] = {
                                'current_value': current_value,
                                'previous_value': prev_value,
                                'change': change,
                                'percent_change': percent_change,
                                'trend': 'increasing' if change > 0 else 'decreasing' if change < 0 else 'stable'
                            }
                            
                            # Identify significant changes (>20% change)
                            if abs(percent_change) > 20:
                                comparison_results['significant_changes'].append({
                                    'parameter': param,
                                    'change': change,
                                    'percent_change': percent_change
                                })
                            elif abs(percent_change) < 5:
                                comparison_results['stable_parameters'].append(param)
                    else:
                        comparison_results['new_parameters'].append(param)
                
                break  # Use only the most recent result for comparison
            
            return {
                'success': True,
                'comparison': comparison_results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Comparison error: {str(e)}',
                'comparison': {}
            }
    
    def _calculate_confidence_score(self, result_data: Dict[str, Any]) -> float:
        """Calculate confidence score based on processing results."""
        try:
            score = 0.0
            
            # Base score for successful processing
            if not result_data.get('error'):
                score += 0.3
            
            # Score based on number of parameters extracted
            params_count = len(result_data.get('lab_results', {}))
            if params_count > 0:
                score += min(0.4, params_count * 0.05)  # Max 0.4 for parameters
            
            # Score based on normal ranges found
            ranges_count = len(result_data.get('lab_normal_ranges', {}))
            if ranges_count > 0:
                score += min(0.2, ranges_count * 0.02)  # Max 0.2 for ranges
            
            # Score based on patient info extraction
            patient_info = result_data.get('patient_info', {})
            if patient_info:
                score += len(patient_info) * 0.025  # Small boost for patient info
            
            return min(1.0, score)  # Cap at 1.0
            
        except Exception:
            return 0.5  # Default moderate confidence
    
    def _save_to_database(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save processed lab data to database."""
        try:
            from healthapp.models import LabResult, User
            from django.shortcuts import get_object_or_404
            from datetime import datetime
            
            user = get_object_or_404(User, id=self.user_id)
            
            # Convert date strings to date objects
            lab_date = result_data.get('lab_date_conducted')
            if isinstance(lab_date, str):
                try:
                    lab_date = datetime.strptime(lab_date, '%Y-%m-%d').date()
                except ValueError:
                    lab_date = datetime.now().date()
            
            recommendation_date = result_data.get('recommendation_date')
            if isinstance(recommendation_date, str):
                try:
                    recommendation_date = datetime.strptime(recommendation_date, '%Y-%m-%d').date()
                except ValueError:
                    recommendation_date = datetime.now().date()
            
            # Create lab result record
            lab_result = LabResult.objects.create(
                user=user,
                lab_test_name=result_data.get('lab_test_name', 'Lab Report'),
                lab_date_conducted=lab_date,
                lab_results=result_data.get('lab_results', {}),
                lab_normal_ranges=result_data.get('lab_normal_ranges', {}),
                interpretation_summary=result_data.get('interpretation_summary', ''),
                interpretation_abnormalities=result_data.get('interpretation_abnormalities', []),
                recommendation_date=recommendation_date,
                recommendation_action=result_data.get('recommendation_action', '')
            )
            
            return {
                'database_saved': True,
                'lab_result_id': lab_result.id,
                'database_message': 'Lab results saved to database successfully.'
            }
            
        except Exception as e:
            return {
                'database_saved': False,
                'database_error': str(e),
                'database_message': 'Failed to save lab results to database.'
            }


# CrewAI Tool Wrapper
class LabReportProcessorTool:
    """
    CrewAI compatible tool wrapper for lab report processing.
    """
    
    def __init__(self, user_id: int = 1):
        self.processor = IntegratedLabReportTool(user_id)
    
    def process_lab_image(self, image_path: str) -> str:
        """
        Tool function to process lab report image.
        Returns formatted string for agent consumption.
        """
        try:
            result = self.processor.process_lab_image_from_path(image_path)
            
            if not result['success']:
                return f"❌ Error processing lab image: {result['error']}"
            
            # Format results for agent
            summary = f"✅ Lab Report Processed Successfully\n\n"
            summary += f"📋 Test: {result['lab_test_name']}\n"
            summary += f"📅 Date: {result['lab_date_conducted']}\n"
            summary += f"🔢 Parameters Extracted: {result.get('parameters_extracted', 0)}\n"
            summary += f"⚡ Confidence: {result.get('confidence_score', 0):.2f}\n\n"
            
            # Add key findings
            if result.get('interpretation_abnormalities'):
                summary += "🚨 Abnormal Values:\n"
                for abnormal in result['interpretation_abnormalities'][:3]:  # Limit to top 3
                    summary += f"  • {abnormal}\n"
                summary += "\n"
            
            summary += f"💡 Summary: {result['interpretation_summary']}\n"
            
            if result.get('recommendation_action'):
                summary += f"📝 Recommendations: {result['recommendation_action']}"
            
            return summary
            
        except Exception as e:
            return f"❌ Tool error: {str(e)}"
    
    def get_lab_history(self, test_name: str = None) -> str:
        """
        Tool function to get lab history.
        Returns formatted string for agent consumption.
        """
        try:
            result = self.processor.get_existing_lab_data(test_name)
            
            if not result['success']:
                return f"❌ Error retrieving lab history: {result['error']}"
            
            if not result['data']:
                return "📝 No previous lab results found in database."
            
            summary = f"📊 Lab History ({result['count']} results)\n\n"
            
            for idx, lab_result in enumerate(result['data'][:3], 1):  # Show top 3
                summary += f"{idx}. {lab_result.get('test_name', 'Lab Test')}\n"
                summary += f"   Date: {lab_result.get('date_conducted', 'Unknown')}\n"
                summary += f"   Parameters: {len(lab_result.get('results', {}))}\n"
                if lab_result.get('abnormalities'):
                    summary += f"   Abnormalities: {len(lab_result['abnormalities'])}\n"
                summary += "\n"
            
            return summary
            
        except Exception as e:
            return f"❌ Tool error: {str(e)}"


# Example usage and testing
if __name__ == "__main__":
    print("🔬 Integrated Lab Report Processing Tool")
    print("=" * 50)
    
    # Initialize tool
    tool = IntegratedLabReportTool(user_id=1)
    
    # Check status
    status = tool.get_processing_status()
    print(f"📊 Processing Status:")
    print(f"  Image Processing: {'✅' if status['image_processing_available'] else '❌'}")
    print(f"  Database Integration: {'✅' if status['database_integration_available'] else '❌'}")
    print(f"  Features: {', '.join(status['features'])}")
    print()
    
    # Example for CrewAI integration
    crew_tool = LabReportProcessorTool(user_id=1)
    print("🤖 CrewAI Tool Ready")
    print("Example usage in agent:")
    print('result = crew_tool.process_lab_image("path/to/lab_report.jpg")')
    print('history = crew_tool.get_lab_history("Blood Chemistry")')