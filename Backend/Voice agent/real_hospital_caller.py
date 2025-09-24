import os
from twilio.rest import Client
from dotenv import load_dotenv
import json

load_dotenv()


class HospitalCaller:
    def __init__(self):
        # Initialize Twilio client
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

        if not all([account_sid, auth_token, self.twilio_number]):
            raise Exception("Missing Twilio credentials in .env file")

        self.client = Client(account_sid, auth_token)

    def call_hospital(self, hospital_number, patient_data):
        """Make an actual call to a hospital"""
        print(f"🏥 Calling hospital at {hospital_number}...")
        print(f"📋 Patient: {patient_data['name']}")
        print(f"🔄 Symptoms: {patient_data['symptoms']}")

        # Create TwiML that will connect to your WebSocket server
        webhook_url = (
            os.getenv("NGROK_URL", "https://your-ngrok-url.ngrok.io") + "/voice"
        )

        try:
            call = self.client.calls.create(
                from_=self.twilio_number,
                to=hospital_number,
                url=webhook_url,  # This points to your voice agent
                method="POST",
            )

            print(f"✅ Call initiated! Call SID: {call.sid}")
            print(f"📞 Status: {call.status}")

            return {
                "success": True,
                "call_sid": call.sid,
                "status": call.status,
                "message": f"Call to {hospital_number} initiated successfully",
            }

        except Exception as e:
            print(f"❌ Call failed: {str(e)}")
            return {"success": False, "error": str(e)}


def collect_patient_info():
    """Collect patient information for hospital call"""
    print("=== Nexus Health Assistant - Real Hospital Calling ===\n")

    patient_data = {
        "name": input("Patient full name: "),
        "dob": input("Date of birth (MM/DD/YYYY): "),
        "phone": input("Patient phone number: "),
        "email": input("Patient email: "),
        "symptoms": input("Current symptoms/medical concerns: "),
        "specialist_type": input("Type of specialist needed (e.g., cardiologist): "),
        "urgency": input("Urgency level (routine/urgent/same-day): "),
        "insurance": input("Insurance provider: "),
        "preferred_times": input("Preferred appointment times: "),
    }

    return patient_data


def make_hospital_call():
    """Main function to collect info and make hospital call"""
    try:
        # Collect patient information
        patient_data = collect_patient_info()

        # Get hospital number
        hospital_number = input("\nHospital phone number to call: ")

        # Show summary
        print(f"\n=== Call Summary ===")
        print(f"Patient: {patient_data['name']}")
        print(f"Symptoms: {patient_data['symptoms']}")
        print(f"Specialist: {patient_data['specialist_type']}")
        print(f"Urgency: {patient_data['urgency']}")
        print(f"Calling: {hospital_number}")

        # Confirm
        confirm = input(f"\n⚠️  READY TO MAKE REAL CALL to {hospital_number}? (y/n): ")

        if confirm.lower() != "y":
            print("❌ Call cancelled.")
            return

        # Initialize caller and make the call
        caller = HospitalCaller()
        result = caller.call_hospital(hospital_number, patient_data)

        if result["success"]:
            print(f"\n🎉 SUCCESS! Hospital call initiated.")
            print(f"📞 Call ID: {result['call_sid']}")
            print(f"🤖 Your AI agent is now speaking with the hospital!")
            print(f"\n💬 The AI will say:")
            print(f"   'Hello, this is Nexus Health Assistant calling on behalf of")
            print(f"    {patient_data['name']} who needs to schedule an appointment...")
        else:
            print(f"\n❌ FAILED: {result['error']}")

    except Exception as e:
        print(f"\n⚠️  Setup Error: {e}")
        print(f"\nYou need to:")
        print(f"1. Sign up for Twilio account at https://www.twilio.com")
        print(f"2. Add Twilio credentials to .env file")
        print(f"3. Set up ngrok for webhooks: ngrok http 5000")
        print(f"4. Update NGROK_URL in .env file")


if __name__ == "__main__":
    make_hospital_call()
