#!/usr/bin/env python3
"""
Nexus Health Assistant - Hospital Appointment Booking System
Usage: python book_appointment.py
"""

import requests
import json


def book_hospital_appointment():
    """Collect patient information and trigger hospital call"""

    print("=== Nexus Health Assistant - Appointment Booking ===\n")

    # Collect patient information
    print("Please provide patient information:")
    patient_data = {
        "name": input("Patient full name: "),
        "dob": input("Date of birth (MM/DD/YYYY): "),
        "phone": input("Phone number: "),
        "email": input("Email address: "),
        "symptoms": input("Current symptoms/medical concerns: "),
        "specialist_type": input(
            "Type of specialist needed (e.g., cardiologist, general): "
        ),
        "urgency": input("Urgency level (routine/urgent/same-day): "),
        "insurance": input("Insurance provider: "),
        "preferred_times": input("Preferred appointment times: "),
        "hospital_number": input("Hospital phone number to call: "),
    }

    print(f"\n=== Booking Summary ===")
    print(f"Patient: {patient_data['name']}")
    print(f"Symptoms: {patient_data['symptoms']}")
    print(f"Specialist: {patient_data['specialist_type']}")
    print(f"Urgency: {patient_data['urgency']}")
    print(f"Calling: {patient_data['hospital_number']}")

    confirm = input("\nProceed with hospital call? (y/n): ")

    if confirm.lower() != "y":
        print("Appointment booking cancelled.")
        return

    # Trigger the hospital call (you would call your Flask API here)
    print(f"\n🤖 Nexus AI Agent is now calling {patient_data['hospital_number']}")
    print("📞 Connecting to hospital...")
    print(
        "🗣️  'Hello, this is Nexus Health Assistant calling on behalf of a patient...'"
    )
    print("\n✅ Call in progress. The AI agent will:")
    print("   1. Introduce itself professionally")
    print("   2. Present patient information and symptoms")
    print("   3. Request appointment availability")
    print("   4. Confirm all appointment details")
    print("   5. Provide callback information")

    # In a real implementation, you would make this API call:
    # response = requests.post("http://localhost:5001/book-appointment", json=patient_data)

    print(f"\n📋 Appointment booking initiated for {patient_data['name']}")
    print("📧 Patient will receive confirmation details once call is complete.")


if __name__ == "__main__":
    book_hospital_appointment()
