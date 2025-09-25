"""
Appointment API Test Script

This script demonstrates how to use the appointment endpoints to store and retrieve appointment data.
"""

import requests
import json
from datetime import datetime, timedelta

# API Base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_appointment_api():
    """Test the appointment endpoints"""
    
    # First, you need to register/login to get a token
    # For this demo, we'll assume you have a token
    # Replace this with your actual JWT token
    JWT_TOKEN = "your_jwt_token_here"
    
    print("🏥 Testing Appointment API")
    print("=" * 50)
    
    # Test data for storing an appointment
    appointment_data = {
        "token": JWT_TOKEN,
        "appointment_date": "2025-09-30T14:30:00Z",  # ISO format with timezone
        "location": "City Medical Center, 123 Healthcare Blvd, New York, NY 10001",
        "doctor_name": "Dr. Sarah Johnson",
        "doctor_specialization": "Cardiology", 
        "appointment_type": "consultant",
        "reason": "Follow-up for heart murmur detected during routine checkup"
    }
    
    # 1. Store appointment
    print("\n1. Storing appointment...")
    try:
        response = requests.post(f"{BASE_URL}/appointments/store/", json=appointment_data)
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Success! Appointment stored:")
            print(f"   ID: {data['data']['id']}")
            print(f"   Doctor: {data['data']['doctor_name']} ({data['data']['doctor_specialization']})")
            print(f"   Date: {data['data']['appointment_date']}")
            print(f"   Type: {data['data']['appointment_type']}")
            print(f"   Location: {data['data']['location']}")
            print(f"   Reason: {data['data']['reason']}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure your Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # 2. Get appointments
    print("\n" + "=" * 50)
    print("\n2. Retrieving appointments...")
    try:
        response = requests.post(f"{BASE_URL}/appointments/get/", json={"token": JWT_TOKEN})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data['count']} appointment(s) for user: {data['user']}")
            
            if data['appointments']:
                print("\nAppointment details:")
                for i, appointment in enumerate(data['appointments'], 1):
                    date_obj = datetime.fromisoformat(appointment['appointment_date'].replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%B %d, %Y at %I:%M %p')
                    
                    print(f"\n   {i}. {appointment['doctor_name']} - {appointment['doctor_specialization']}")
                    print(f"      📅 Date: {formatted_date}")
                    print(f"      📍 Location: {appointment['location']}")
                    print(f"      🏷️  Type: {appointment['appointment_type'].title()}")
                    print(f"      📝 Reason: {appointment['reason']}")
                    print(f"      🆔 ID: {appointment['id']}")
            else:
                print("No appointments found.")
                
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure your Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def print_api_documentation():
    """Print API documentation for the appointment endpoints"""
    
    print("\n" + "=" * 50)
    print("📚 Appointment API Documentation")
    print("=" * 50)
    
    print("\n🔗 Store Appointment")
    print("POST /api/appointments/store/")
    print("Headers: Content-Type: application/json")
    print("\nRequest Body:")
    example_store = {
        "token": "your_jwt_token_here",
        "appointment_date": "2025-09-30T14:30:00Z",
        "location": "City Medical Center, 123 Healthcare Blvd, NY",
        "doctor_name": "Dr. Sarah Johnson", 
        "doctor_specialization": "Cardiology",
        "appointment_type": "consultant",  # or "general"
        "reason": "Follow-up for heart murmur"
    }
    print(json.dumps(example_store, indent=2))
    
    print("\n🔗 Get Appointments") 
    print("POST /api/appointments/get/")
    print("Headers: Content-Type: application/json")
    print("\nRequest Body:")
    example_get = {
        "token": "your_jwt_token_here"
    }
    print(json.dumps(example_get, indent=2))
    
    print("\n📋 Field Descriptions:")
    print("• token: JWT authentication token (required)")
    print("• appointment_date: Date and time in ISO format (required)")
    print("• location: Full address or location name (required)")
    print("• doctor_name: Full name of the doctor (required)")
    print("• doctor_specialization: Medical specialization (required)")
    print("• appointment_type: 'general' or 'consultant' (required)")
    print("• reason: Purpose of the appointment (required)")
    
    print("\n🎯 Appointment Types:")
    print("• general: Regular checkups, basic consultations")
    print("• consultant: Specialist consultations, follow-ups")
    
    print("\n💡 Example Specializations:")
    print("• Cardiology, Dermatology, Neurology, Orthopedics")
    print("• Pediatrics, Psychiatry, Radiology, Oncology")
    print("• Internal Medicine, Family Medicine, etc.")

if __name__ == "__main__":
    # Print documentation
    print_api_documentation()
    
    # Note: To actually test the API, you need to:
    # 1. Start the Django server: python manage.py runserver
    # 2. Register/login to get a JWT token
    # 3. Replace JWT_TOKEN variable with your actual token
    # 4. Run this script
    
    print("\n" + "=" * 50)
    print("🚀 To test the API:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Register/login to get JWT token")
    print("3. Replace JWT_TOKEN in this script")
    print("4. Run: python test_appointments.py")
    
    # Uncomment the line below and add your token to test
    # test_appointment_api()