from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from datetime import datetime, date
from .services import DataOrInputHandler, HealthDataService


@csrf_exempt
@require_http_methods(["GET", "POST"])
def user_profile_data_or_input(request):
    """
    API endpoint to get user profile from database or handle user input.
    GET: Returns existing profile or indicates input needed
    POST: Creates/updates profile with user input
    """
    try:
        # For demo purposes, using user_id from request. In production, use request.user.id
        user_id = request.GET.get('user_id') or request.POST.get('user_id', 1)
        handler = DataOrInputHandler(user_id)
        
        if request.method == 'GET':
            # Try to get existing profile
            profile_data = handler.get_user_profile_or_input()
            return JsonResponse({
                'success': True,
                'data': profile_data
            })
        
        elif request.method == 'POST':
            # Handle user input
            data = json.loads(request.body)
            user_input = {
                'age': data.get('age'),
                'phone': data.get('phone'),
                'emergency_contact': data.get('emergency_contact')
            }
            
            # Create/update profile with user input
            profile_data = HealthDataService.get_or_create_user_profile(user_id, user_input)
            
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully',
                'data': profile_data
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def medicine_data_or_input(request):
    """
    API endpoint to get medicine data from database or handle user input.
    GET: Returns existing medicine records or indicates input needed
    POST: Creates new medicine record with user input
    """
    try:
        user_id = request.GET.get('user_id') or request.POST.get('user_id', 1)
        handler = DataOrInputHandler(user_id)
        
        if request.method == 'GET':
            medicine_name = request.GET.get('medicine_name')
            medicine_data = handler.get_medicine_data_or_input(medicine_name)
            return JsonResponse({
                'success': True,
                'data': medicine_data
            })
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['medicine_name', 'medicine_dosage', 'medicine_frequency', 
                             'medicine_timing', 'medicine_quantity_available']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }, status=400)
            
            # Handle date conversion if provided
            if 'restock_date' in data and data['restock_date']:
                try:
                    data['restock_date'] = datetime.strptime(data['restock_date'], '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid date format for restock_date. Use YYYY-MM-DD.'
                    }, status=400)
            
            saved_record = HealthDataService.save_medicine_record(user_id, data)
            
            return JsonResponse({
                'success': True,
                'message': 'Medicine record saved successfully',
                'data': saved_record
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def appointment_data_or_input(request):
    """
    API endpoint to get appointment history from database or handle new appointment input.
    GET: Returns existing appointments or indicates input needed
    POST: Creates new appointment with user input
    """
    try:
        user_id = request.GET.get('user_id') or request.POST.get('user_id', 1)
        handler = DataOrInputHandler(user_id)
        
        if request.method == 'GET':
            appointment_data = handler.get_appointment_history_or_input()
            return JsonResponse({
                'success': True,
                'data': appointment_data
            })
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['user_symptoms', 'assessment_urgency_level', 'hospital_name', 
                             'hospital_address', 'hospital_distance_km', 'appointment_status',
                             'appointment_doctor', 'appointment_department', 'appointment_date', 
                             'appointment_time', 'confirmation_message']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }, status=400)
            
            # Handle date and time conversion
            try:
                data['appointment_date'] = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
                data['appointment_time'] = datetime.strptime(data['appointment_time'], '%H:%M').time()
            except ValueError as e:
                return JsonResponse({
                    'success': False,
                    'error': f'Invalid date/time format: {str(e)}'
                }, status=400)
            
            saved_appointment = HealthDataService.save_appointment(user_id, data)
            
            return JsonResponse({
                'success': True,
                'message': 'Appointment saved successfully',
                'data': saved_appointment
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def lab_results_data(request):
    """
    API endpoint to get lab results from database.
    """
    try:
        user_id = request.GET.get('user_id', 1)
        test_name = request.GET.get('test_name')
        
        lab_results = HealthDataService.get_lab_results(user_id, test_name)
        
        if not lab_results:
            return JsonResponse({
                'success': True,
                'data': {
                    'needs_input': True,
                    'message': f'No lab results found{"" if not test_name else f" for {test_name}"}.'
                }
            })
        
        return JsonResponse({
            'success': True,
            'data': {
                'found_in_database': True,
                'results': lab_results,
                'count': len(lab_results)
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def check_data_availability(request):
    """
    API endpoint to check what data is available in database for a user.
    Returns a summary of available data and what needs user input.
    """
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id', 1)
        
        handler = DataOrInputHandler(user_id)
        
        # Check profile data
        profile_data = handler.get_user_profile_or_input()
        
        # Check medicine data
        medicine_data = handler.get_medicine_data_or_input()
        
        # Check appointment data
        appointment_data = handler.get_appointment_history_or_input()
        
        # Check lab results
        lab_results = HealthDataService.get_lab_results(user_id)
        
        summary = {
            'user_profile': {
                'available': not profile_data.get('needs_input', False),
                'complete': bool(profile_data.get('user_age')),
                'data': profile_data if not profile_data.get('needs_input') else None
            },
            'medicines': {
                'available': medicine_data.get('found_in_database', False),
                'count': medicine_data.get('count', 0),
                'needs_input': medicine_data.get('needs_input', False)
            },
            'appointments': {
                'available': appointment_data.get('found_in_database', False),
                'count': appointment_data.get('count', 0),
                'needs_input': appointment_data.get('needs_input', False)
            },
            'lab_results': {
                'available': len(lab_results) > 0,
                'count': len(lab_results)
            }
        }
        
        return JsonResponse({
            'success': True,
            'data': summary
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)