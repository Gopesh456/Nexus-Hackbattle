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

    def call_hospital(self, to_number, patient_data=None):
        """Make an actual outbound call using Twilio
        
        Args:
            to_number (str): Phone number to call (must include country code, e.g., +1234567890)
            patient_data (dict, optional): Patient information for context
        
        Returns:
            dict: Call result with success status and details
        """
        print(f"🏥 Initiating outbound call to {to_number}...")
        
        if patient_data:
            print(f"📋 Patient: {patient_data.get('name', 'N/A')}")
            print(f"🔄 Symptoms: {patient_data.get('symptoms', 'N/A')}")

        # Validate phone numbers
        if not to_number or not to_number.startswith('+'):
            return {
                "success": False, 
                "error": "Invalid 'to' phone number. Must include country code (e.g., +1234567890)"
            }
            
        if not self.twilio_number or not self.twilio_number.startswith('+'):
            return {
                "success": False, 
                "error": "Invalid Twilio phone number configuration in .env file"
            }

        # Get webhook URL from environment
        ngrok_url = os.getenv("NGROK_URL")
        if not ngrok_url:
            return {
                "success": False, 
                "error": "NGROK_URL not configured in .env file"
            }
            
        # Clean up webhook URL
        webhook_url = ngrok_url.replace('https://', '').replace('http://', '')
        webhook_url = f"https://{webhook_url}/voice"

        try:
            print(f"📞 FROM: {self.twilio_number} (Your Twilio Number)")
            print(f"📞 TO: {to_number} (Destination)")
            print(f"🔗 Webhook: {webhook_url}")
            
            # Make the outbound call
            call = self.client.calls.create(
                from_=self.twilio_number,  # Your Twilio number (source)
                to=to_number,             # Destination number
                url=webhook_url,          # Your voice agent webhook
                method="POST",
                timeout=30,               # Ring timeout
                record=False              # Set to True to record calls
            )

            print(f"✅ Call initiated successfully!")
            print(f"🆔 Call SID: {call.sid}")
            print(f"� Initial Status: {call.status}")

            return {
                "success": True,
                "call_sid": call.sid,
                "status": call.status,
                "from_number": self.twilio_number,
                "to_number": to_number,
                "webhook_url": webhook_url,
                "message": f"Outbound call from {self.twilio_number} to {to_number} initiated successfully"
            }

        except Exception as e:
            error_msg = f"Twilio API Error: {str(e)}"
            print(f"❌ Call failed: {error_msg}")
            return {
                "success": False, 
                "error": error_msg,
                "from_number": self.twilio_number,
                "to_number": to_number
            }


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
