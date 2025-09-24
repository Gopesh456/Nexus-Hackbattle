#!/usr/bin/env python3
"""
Nexus Health Assistant - Hospital Appointment Booking System - TEST VERSION
"""


def test_appointment_booking():
    """Test the appointment booking flow with sample data"""

    print("=== Nexus Health Assistant - Appointment Booking TEST ===\n")

    # Sample patient information
    patient_data = {
        "name": "John Doe",
        "dob": "01/15/1980",
        "phone": "+1234567890",
        "email": "john.doe@email.com",
        "symptoms": "chest pain, shortness of breath",
        "specialist_type": "cardiologist",
        "urgency": "urgent",
        "insurance": "Blue Cross Blue Shield",
        "preferred_times": "Monday-Wednesday mornings",
        "hospital_number": "+1555123456",
    }

    print("🏥 TESTING HOSPITAL APPOINTMENT BOOKING SYSTEM")
    print("=" * 50)

    print(f"\n📋 PATIENT INFORMATION:")
    print(f"   Name: {patient_data['name']}")
    print(f"   DOB: {patient_data['dob']}")
    print(f"   Phone: {patient_data['phone']}")
    print(f"   Email: {patient_data['email']}")
    print(f"   Symptoms: {patient_data['symptoms']}")
    print(f"   Specialist Needed: {patient_data['specialist_type']}")
    print(f"   Urgency: {patient_data['urgency']}")
    print(f"   Insurance: {patient_data['insurance']}")
    print(f"   Preferred Times: {patient_data['preferred_times']}")
    print(f"   Hospital Number: {patient_data['hospital_number']}")

    print(f"\n🤖 NEXUS AI AGENT SIMULATION:")
    print("=" * 50)
    print("📞 Dialing hospital number: +1555123456")
    print("🔊 Ring... Ring... Ring...")
    print("👩‍⚕️ Hospital: 'Hello, St. Mary's Hospital, how can I help you?'")
    print()

    print("🤖 Nexus Agent: 'Hello, this is Nexus Health Assistant calling on")
    print("   behalf of a patient who needs to schedule an appointment.")
    print("   May I speak with someone who handles appointment scheduling?'")
    print()

    print("👩‍⚕️ Hospital: 'Yes, this is Sarah in scheduling. How can I help?'")
    print()

    print("🤖 Nexus Agent: 'Thank you Sarah. I'm calling for John Doe,")
    print(f"   date of birth {patient_data['dob']}. The patient is experiencing")
    print(
        f"   {patient_data['symptoms']} and needs to see a {patient_data['specialist_type']}."
    )
    print(f"   This is an {patient_data['urgency']} case.'")
    print()

    print("👩‍⚕️ Hospital: 'I understand. Let me check our cardiology availability...")
    print("   We have an opening tomorrow at 2:00 PM with Dr. Martinez.'")
    print()

    print("🤖 Nexus Agent: 'That works perfectly. Could you please confirm:")
    print("   - Date: Tomorrow, 2:00 PM")
    print("   - Doctor: Dr. Martinez")
    print("   - Department: Cardiology")
    print(f"   The patient has {patient_data['insurance']} insurance and can be")
    print(f"   reached at {patient_data['phone']} if needed.'")
    print()

    print("👩‍⚕️ Hospital: 'Confirmed! Please have the patient arrive 15 minutes")
    print("   early with their insurance card and ID.'")
    print()

    print("🤖 Nexus Agent: 'Perfect! Thank you Sarah. I'll inform the patient")
    print("   immediately. Should they call this number if they need to reschedule?'")
    print()

    print("👩‍⚕️ Hospital: 'Yes, or they can call our main line. Have a great day!'")
    print()

    print("✅ APPOINTMENT SUCCESSFULLY BOOKED!")
    print("=" * 50)
    print("📅 Appointment Details:")
    print("   • Patient: John Doe")
    print("   • Date: Tomorrow, 2:00 PM")
    print("   • Doctor: Dr. Martinez (Cardiology)")
    print("   • Location: St. Mary's Hospital")
    print("   • Instructions: Arrive 15 minutes early with insurance card and ID")
    print()

    print("📧 Next Steps:")
    print("   • Patient will receive confirmation SMS")
    print("   • Reminder call 24 hours before appointment")
    print("   • Emergency contact: Hospital main line")
    print()

    print("🎉 Nexus Health Assistant - Appointment Booking Complete!")


if __name__ == "__main__":
    test_appointment_booking()
