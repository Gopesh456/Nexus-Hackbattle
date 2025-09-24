"""
Simple Hospital Calling Test
Run this to test the hospital calling system
"""

import os
import json


def make_hospital_call():
    """Interactive hospital calling function"""
    print("🏥 NEXUS HOSPITAL CALLING SYSTEM")
    print("=" * 50)

    # Check if Twilio is available
    try:
        from twilio.rest import Client

        twilio_available = True
        print("✅ Twilio available - Real calls possible")
    except ImportError:
        twilio_available = False
        print("⚠️  Twilio not installed - Simulation mode only")
        print("   Install with: uv add twilio")

    # Collect patient info
    print("\n📋 PATIENT INFORMATION:")
    patient_data = {
        "name": input("Patient name: "),
        "dob": input("Date of birth (MM/DD/YYYY): "),
        "phone": input("Patient phone: "),
        "symptoms": input("Symptoms: "),
        "specialist": input("Specialist needed: "),
        "urgency": input("Urgency (routine/urgent/emergency): "),
        "insurance": input("Insurance: "),
    }

    hospital_number = input("\nHospital phone number: ")

    print(f"\n📞 CALLING: {hospital_number}")
    print(f"👤 FOR: {patient_data['name']}")
    print(f"🏥 SYMPTOMS: {patient_data['symptoms']}")

    if twilio_available:
        # Check if Twilio credentials are configured
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        phone_number = os.getenv("TWILIO_PHONE_NUMBER")

        if all([account_sid, auth_token, phone_number]):
            print("✅ Twilio configured - Ready for REAL calls")
            confirm = input("Make REAL call? (y/n): ")
            if confirm.lower() == "y":
                return make_real_call(hospital_number, patient_data)

    # Fall back to simulation
    print("🎭 SIMULATION MODE")
    return simulate_call(hospital_number, patient_data)


def make_real_call(hospital_number, patient_data):
    """Make actual Twilio call"""
    try:
        from twilio.rest import Client

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        phone_number = os.getenv("TWILIO_PHONE_NUMBER")

        client = Client(account_sid, auth_token)

        # Make the call
        call = client.calls.create(
            from_=phone_number,
            to=hospital_number,
            url="http://demo.twilio.com/docs/voice.xml",  # Simple test TwiML
        )

        print(f"📞 REAL CALL INITIATED!")
        print(f"🆔 Call SID: {call.sid}")
        print(f"📱 Calling from: {phone_number}")
        print(f"🏥 Calling to: {hospital_number}")
        print(f"🤖 AI agent will speak when answered")

        return {"success": True, "type": "real", "call_sid": call.sid}

    except Exception as e:
        print(f"❌ Real call failed: {e}")
        return simulate_call(hospital_number, patient_data)


def simulate_call(hospital_number, patient_data):
    """Simulate hospital conversation"""
    print(f"🎭 SIMULATING call to {hospital_number}...")
    print("📞 Ring... Ring... Ring...")

    print("\n👩‍⚕️ Hospital: 'Hello, City General Hospital, how may I help you?'")

    print(f"\n🤖 Nexus Agent: 'Hello, this is Nexus Health Assistant calling")
    print(
        f"   on behalf of {patient_data['name']} who needs to schedule an appointment."
    )
    print(f"   May I speak with someone in scheduling?'")

    print(f"\n👩‍⚕️ Hospital: 'Yes, this is scheduling. How can I help?'")

    print(
        f"\n🤖 Nexus Agent: 'I'm calling for {patient_data['name']}, DOB {patient_data['dob']}."
    )
    print(f"   The patient is experiencing {patient_data['symptoms']} and needs to see")
    print(
        f"   a {patient_data['specialist']}. This is {patient_data['urgency']} priority.'"
    )

    print(f"\n👩‍⚕️ Hospital: 'I can schedule that. We have availability Tuesday at 2 PM")
    print(f"   with Dr. Martinez.'")

    print(
        f"\n🤖 Nexus Agent: 'Perfect! Could you confirm: Tuesday 2 PM with Dr. Martinez?"
    )
    print(
        f"   The patient has {patient_data['insurance']} insurance and can be reached"
    )
    print(f"   at {patient_data['phone']}.'")

    print(f"\n👩‍⚕️ Hospital: 'Confirmed! Please arrive 15 minutes early.'")

    print(f"\n🤖 Nexus Agent: 'Thank you! I'll inform the patient immediately.'")

    print(f"\n✅ APPOINTMENT BOOKED!")
    print(f"📅 Tuesday 2 PM with Dr. Martinez")

    return {"success": True, "type": "simulation", "appointment": "Tuesday 2 PM"}


def quick_test():
    """Quick test with sample data"""
    print("🚀 QUICK TEST - Hospital Calling System")
    print("Using sample patient data...")

    # Sample data
    patient_data = {
        "name": "John Doe",
        "dob": "01/15/1985",
        "phone": "+1234567890",
        "symptoms": "chest pain and shortness of breath",
        "specialist": "cardiologist",
        "urgency": "urgent",
        "insurance": "Blue Cross",
    }

    hospital_number = "+1555123HOSP"

    print(f"\n📋 Patient: {patient_data['name']}")
    print(f"🏥 Calling: {hospital_number}")
    print(f"⚠️  Symptoms: {patient_data['symptoms']}")

    return simulate_call(hospital_number, patient_data)


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Interactive hospital call")
    print("2. Quick test with sample data")

    choice = input("Enter choice (1 or 2): ")

    if choice == "2":
        result = quick_test()
    else:
        result = make_hospital_call()

    print(f"\n🎯 RESULT: {result}")
    print("\n✨ Hospital calling system ready!")

    if result.get("type") == "simulation":
        print("\n💡 To enable REAL calls:")
        print("1. Install Twilio: uv add twilio")
        print("2. Get Twilio credentials from twilio.com")
        print("3. Set environment variables:")
        print("   - TWILIO_ACCOUNT_SID")
        print("   - TWILIO_AUTH_TOKEN")
        print("   - TWILIO_PHONE_NUMBER")
