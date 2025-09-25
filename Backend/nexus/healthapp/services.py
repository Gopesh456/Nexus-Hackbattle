from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import UserProfile, MedicineRecord, HealthAlert, LabResult, Appointment
from typing import Optional, Dict, Any, List


class HealthDataService:
    """
    Service class to handle database operations for health data.
    Implements the pattern: get from database, if not found take user input.
    """

    @staticmethod
    def get_or_create_user_profile(user_id: int, user_input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get user profile from database or create with user input.
        
        Args:
            user_id: The user's ID
            user_input_data: Data from user input if profile doesn't exist
            
        Returns:
            Dictionary containing user profile data
        """
        try:
            user = get_object_or_404(User, id=user_id)
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'age': user_input_data.get('age') if user_input_data else None,
                    'phone': user_input_data.get('phone') if user_input_data else None,
                    'emergency_contact': user_input_data.get('emergency_contact') if user_input_data else None,
                }
            )
            
            return {
                'user_name': user.first_name or user.username,
                'user_age': profile.age,
                'phone': profile.phone,
                'emergency_contact': profile.emergency_contact,
                'is_new_profile': created
            }
        except Exception as e:
            raise Exception(f"Error getting/creating user profile: {e}")

    @staticmethod
    def get_medicine_records(user_id: int, medicine_name: str = None) -> List[Dict[str, Any]]:
        """
        Get medicine records from database.
        
        Args:
            user_id: The user's ID
            medicine_name: Optional specific medicine name to filter
            
        Returns:
            List of medicine records or empty list if none found
        """
        try:
            user = get_object_or_404(User, id=user_id)
            queryset = MedicineRecord.objects.filter(user=user)
            
            if medicine_name:
                queryset = queryset.filter(medicine_name__icontains=medicine_name)
            
            records = []
            for record in queryset:
                records.append({
                    'medicine_name': record.medicine_name,
                    'medicine_dosage': record.medicine_dosage,
                    'medicine_frequency': record.medicine_frequency,
                    'medicine_timing': record.medicine_timing,
                    'medicine_quantity_available': record.medicine_quantity_available,
                    'medicine_special_instructions': record.medicine_special_instructions,
                    'restock_date': record.restock_date.isoformat() if record.restock_date else None,
                })
            
            return records
        except Exception as e:
            raise Exception(f"Error getting medicine records: {e}")

    @staticmethod
    def save_medicine_record(user_id: int, medicine_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save medicine record to database from user input.
        
        Args:
            user_id: The user's ID
            medicine_data: Medicine data from user input
            
        Returns:
            Saved medicine record data
        """
        try:
            user = get_object_or_404(User, id=user_id)
            
            record = MedicineRecord.objects.create(
                user=user,
                medicine_name=medicine_data['medicine_name'],
                medicine_dosage=medicine_data['medicine_dosage'],
                medicine_frequency=medicine_data['medicine_frequency'],
                medicine_timing=medicine_data['medicine_timing'],
                medicine_quantity_available=medicine_data['medicine_quantity_available'],
                medicine_special_instructions=medicine_data.get('medicine_special_instructions', ''),
                restock_date=medicine_data.get('restock_date')
            )
            
            return {
                'medicine_name': record.medicine_name,
                'medicine_dosage': record.medicine_dosage,
                'medicine_frequency': record.medicine_frequency,
                'medicine_timing': record.medicine_timing,
                'medicine_quantity_available': record.medicine_quantity_available,
                'medicine_special_instructions': record.medicine_special_instructions,
                'restock_date': record.restock_date.isoformat() if record.restock_date else None,
                'message': f'Medicine record for {record.medicine_name} has been saved successfully.'
            }
        except Exception as e:
            raise Exception(f"Error saving medicine record: {e}")

    @staticmethod
    def get_recent_appointments(user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent appointments from database.
        
        Args:
            user_id: The user's ID
            limit: Number of recent appointments to fetch
            
        Returns:
            List of recent appointments or empty list if none found
        """
        try:
            user = get_object_or_404(User, id=user_id)
            appointments = Appointment.objects.filter(user=user).order_by('-appointment_date')[:limit]
            
            records = []
            for appointment in appointments:
                records.append({
                    'user_symptoms': appointment.user_symptoms,
                    'assessment_urgency_level': appointment.assessment_urgency_level,
                    'hospital_name': appointment.hospital_name,
                    'hospital_address': appointment.hospital_address,
                    'hospital_distance_km': appointment.hospital_distance_km,
                    'appointment_status': appointment.appointment_status,
                    'appointment_doctor': appointment.appointment_doctor,
                    'appointment_department': appointment.appointment_department,
                    'appointment_date': appointment.appointment_date.isoformat(),
                    'appointment_time': appointment.appointment_time.strftime('%H:%M'),
                    'confirmation_message': appointment.confirmation_message,
                })
            
            return records
        except Exception as e:
            raise Exception(f"Error getting appointments: {e}")

    @staticmethod
    def save_appointment(user_id: int, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save appointment to database from user input.
        
        Args:
            user_id: The user's ID
            appointment_data: Appointment data from user input
            
        Returns:
            Saved appointment data
        """
        try:
            user = get_object_or_404(User, id=user_id)
            
            appointment = Appointment.objects.create(
                user=user,
                user_symptoms=appointment_data['user_symptoms'],
                assessment_urgency_level=appointment_data['assessment_urgency_level'],
                hospital_name=appointment_data['hospital_name'],
                hospital_address=appointment_data['hospital_address'],
                hospital_distance_km=appointment_data['hospital_distance_km'],
                appointment_status=appointment_data['appointment_status'],
                appointment_doctor=appointment_data['appointment_doctor'],
                appointment_department=appointment_data['appointment_department'],
                appointment_date=appointment_data['appointment_date'],
                appointment_time=appointment_data['appointment_time'],
                confirmation_message=appointment_data['confirmation_message'],
            )
            
            return {
                'appointment_id': appointment.id,
                'user_symptoms': appointment.user_symptoms,
                'assessment_urgency_level': appointment.assessment_urgency_level,
                'hospital_name': appointment.hospital_name,
                'hospital_address': appointment.hospital_address,
                'hospital_distance_km': appointment.hospital_distance_km,
                'appointment_status': appointment.appointment_status,
                'appointment_doctor': appointment.appointment_doctor,
                'appointment_department': appointment.appointment_department,
                'appointment_date': appointment.appointment_date.isoformat(),
                'appointment_time': appointment.appointment_time.strftime('%H:%M'),
                'confirmation_message': appointment.confirmation_message,
                'message': 'Appointment has been saved successfully.'
            }
        except Exception as e:
            raise Exception(f"Error saving appointment: {e}")

    @staticmethod
    def get_lab_results(user_id: int, test_name: str = None) -> List[Dict[str, Any]]:
        """
        Get lab results from database.
        
        Args:
            user_id: The user's ID
            test_name: Optional specific test name to filter
            
        Returns:
            List of lab results or empty list if none found
        """
        try:
            user = get_object_or_404(User, id=user_id)
            queryset = LabResult.objects.filter(user=user)
            
            if test_name:
                queryset = queryset.filter(lab_test_name__icontains=test_name)
            
            records = []
            for result in queryset.order_by('-lab_date_conducted'):
                records.append({
                    'lab_test_name': result.lab_test_name,
                    'lab_date_conducted': result.lab_date_conducted.isoformat(),
                    'lab_results': result.lab_results,
                    'lab_normal_ranges': result.lab_normal_ranges,
                    'interpretation_summary': result.interpretation_summary,
                    'interpretation_abnormalities': result.interpretation_abnormalities,
                    'recommendation_date': result.recommendation_date.isoformat(),
                    'recommendation_action': result.recommendation_action,
                })
            
            return records
        except Exception as e:
            raise Exception(f"Error getting lab results: {e}")


class DataOrInputHandler:
    """
    Main handler class that implements the pattern:
    1. Try to get data from database
    2. If not found, prompt for user input
    3. Save user input to database for future use
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.service = HealthDataService()

    def get_user_profile_or_input(self, prompt_for_input_callback=None) -> Dict[str, Any]:
        """
        Get user profile from database or prompt for input if not found.
        
        Args:
            prompt_for_input_callback: Function to call when user input is needed
            
        Returns:
            User profile data
        """
        try:
            # First, try to get from database
            profile_data = self.service.get_or_create_user_profile(self.user_id)
            
            # If profile is incomplete or new, get user input
            if profile_data['is_new_profile'] or not profile_data['user_age']:
                if prompt_for_input_callback:
                    user_input = prompt_for_input_callback()
                    # Update with user input
                    profile_data = self.service.get_or_create_user_profile(
                        self.user_id, 
                        user_input
                    )
                else:
                    # Return what we have with a flag indicating more input needed
                    profile_data['needs_input'] = True
            
            return profile_data
        except Exception as e:
            raise Exception(f"Error in get_user_profile_or_input: {e}")

    def get_medicine_data_or_input(self, medicine_name: str = None, prompt_for_input_callback=None) -> Dict[str, Any]:
        """
        Get medicine data from database or prompt for input if not found.
        
        Args:
            medicine_name: Specific medicine to look for
            prompt_for_input_callback: Function to call when user input is needed
            
        Returns:
            Medicine data
        """
        try:
            # First, try to get from database
            medicine_records = self.service.get_medicine_records(self.user_id, medicine_name)
            
            if not medicine_records:
                # No records found, need user input
                if prompt_for_input_callback:
                    user_input = prompt_for_input_callback()
                    # Save user input to database
                    saved_record = self.service.save_medicine_record(self.user_id, user_input)
                    return saved_record
                else:
                    return {
                        'needs_input': True,
                        'message': f'No medicine records found{"" if not medicine_name else f" for {medicine_name}"}. Please provide medicine details.'
                    }
            
            # Return existing records
            return {
                'found_in_database': True,
                'records': medicine_records,
                'count': len(medicine_records)
            }
        except Exception as e:
            raise Exception(f"Error in get_medicine_data_or_input: {e}")

    def get_appointment_history_or_input(self, prompt_for_input_callback=None) -> Dict[str, Any]:
        """
        Get appointment history from database or handle new appointment input.
        
        Args:
            prompt_for_input_callback: Function to call for new appointment
            
        Returns:
            Appointment data
        """
        try:
            # Get recent appointments
            recent_appointments = self.service.get_recent_appointments(self.user_id)
            
            if not recent_appointments:
                # No appointment history, this might be a new user
                if prompt_for_input_callback:
                    user_input = prompt_for_input_callback()
                    saved_appointment = self.service.save_appointment(self.user_id, user_input)
                    return saved_appointment
                else:
                    return {
                        'needs_input': True,
                        'message': 'No appointment history found. Ready to book new appointment.'
                    }
            
            return {
                'found_in_database': True,
                'appointments': recent_appointments,
                'count': len(recent_appointments)
            }
        except Exception as e:
            raise Exception(f"Error in get_appointment_history_or_input: {e}")