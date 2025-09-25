#!/usr/bin/env python
"""
Example script demonstrating the database-or-input pattern for health data.

This script shows how to:
1. Check if data exists in database
2. If not found, prompt for user input
3. Save user input to database for future use
4. Use the data in health agents

Run this after setting up the Django models and running migrations.
"""

import os
import sys
import django

# Add the Django project to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'nexus'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus.settings')
django.setup()

from healthapp.services import DataOrInputHandler, HealthDataService
from datetime import datetime, date


def demo_user_profile_flow(user_id: int = 1):
    """
    Demonstrate the user profile data-or-input flow.
    """
    print("=== USER PROFILE DEMO ===")
    handler = DataOrInputHandler(user_id)
    
    # Try to get existing profile
    print("1. Checking for existing user profile...")
    profile_data = handler.get_user_profile_or_input()
    
    if profile_data.get('needs_input') or profile_data.get('is_new_profile'):
        print("2. No complete profile found. Collecting user input...")
        
        # Simulate user input
        user_input = {
            'age': 30,
            'phone': '+1234567890',
            'emergency_contact': 'John Doe - +0987654321'
        }
        
        print(f"   User input: {user_input}")
        
        # Save with user input
        updated_profile = HealthDataService.get_or_create_user_profile(user_id, user_input)
        print(f"3. Profile saved: {updated_profile}")
    else:
        print(f"2. Existing profile found: {profile_data}")
    
    print()


def demo_medicine_flow(user_id: int = 1):
    """
    Demonstrate the medicine data-or-input flow.
    """
    print("=== MEDICINE DATA DEMO ===")
    handler = DataOrInputHandler(user_id)
    
    # Try to get existing medicine data
    print("1. Checking for existing medicine records...")
    medicine_data = handler.get_medicine_data_or_input("Aspirin")
    
    if medicine_data.get('needs_input'):
        print("2. No medicine records found. Collecting user input...")
        
        # Simulate user input
        user_input = {
            'medicine_name': 'Aspirin',
            'medicine_dosage': '100mg',
            'medicine_frequency': '2 times per day',
            'medicine_timing': ['08:00', '20:00'],
            'medicine_quantity_available': 30,
            'medicine_special_instructions': 'Take after meals',
            'restock_date': date(2025, 10, 15)
        }
        
        print(f"   User input: {user_input}")
        
        # Save medicine record
        saved_record = HealthDataService.save_medicine_record(user_id, user_input)
        print(f"3. Medicine record saved: {saved_record}")
    else:
        print(f"2. Existing medicine records found: {medicine_data}")
    
    print()


def demo_appointment_flow(user_id: int = 1):
    """
    Demonstrate the appointment data-or-input flow.
    """
    print("=== APPOINTMENT DATA DEMO ===")
    handler = DataOrInputHandler(user_id)
    
    # Try to get existing appointment data
    print("1. Checking for existing appointments...")
    appointment_data = handler.get_appointment_history_or_input()
    
    if appointment_data.get('needs_input'):
        print("2. No appointments found. Creating new appointment...")
        
        # Simulate user input for new appointment
        user_input = {
            'user_symptoms': ['headache', 'fever', 'fatigue'],
            'assessment_urgency_level': 'medium',
            'hospital_name': 'City General Hospital',
            'hospital_address': '123 Main St, City, State 12345',
            'hospital_distance_km': 5.2,
            'appointment_status': 'confirmed',
            'appointment_doctor': 'Dr. Smith',
            'appointment_department': 'General Medicine',
            'appointment_date': date(2025, 10, 1),
            'appointment_time': datetime.strptime('14:30', '%H:%M').time(),
            'confirmation_message': 'Your appointment with Dr. Smith has been successfully booked for 2025-10-01 at 14:30.'
        }
        
        print(f"   User input: {user_input}")
        
        # Save appointment
        saved_appointment = HealthDataService.save_appointment(user_id, user_input)
        print(f"3. Appointment saved: {saved_appointment}")
    else:
        print(f"2. Existing appointments found: {appointment_data}")
    
    print()


def demo_integration_with_agents():
    """
    Demonstrate how to integrate with health agents.
    """
    print("=== AGENT INTEGRATION DEMO ===")
    
    # Import the integration tool
    from healthguard.tools.database_integration import DatabaseOrInputTool
    
    # Create tool instance
    db_tool = DatabaseOrInputTool(user_id=1)
    
    # Use in agent context
    print("1. Getting patient profile for agent...")
    profile_result = db_tool.get_patient_profile()
    print(f"   Agent received: {profile_result}")
    
    print("2. Getting medicine history for agent...")
    medicine_result = db_tool.get_medicine_history()
    print(f"   Agent received: {medicine_result}")
    
    print()


def main():
    """
    Run all demo flows.
    """
    print("DATABASE-OR-INPUT PATTERN DEMONSTRATION")
    print("=" * 50)
    print()
    
    try:
        demo_user_profile_flow()
        demo_medicine_flow()
        demo_appointment_flow()
        demo_integration_with_agents()
        
        print("✅ All demos completed successfully!")
        print("\nTo run the Django server and test the API endpoints:")
        print("1. cd Backend/nexus")
        print("2. python manage.py makemigrations healthapp")
        print("3. python manage.py migrate")
        print("4. python manage.py runserver")
        print("\nThen you can test the API at http://localhost:8000/healthapp/api/")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        print("\nMake sure to run Django migrations first:")
        print("1. cd Backend/nexus")
        print("2. python manage.py makemigrations healthapp")
        print("3. python manage.py migrate")


if __name__ == "__main__":
    main()