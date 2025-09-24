import asyncio
import base64
import json
import websockets
import os
from dotenv import load_dotenv

load_dotenv()

# Import Twilio if available
try:
    from twilio.rest import Client

    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("⚠️  Twilio not installed. Install with: uv add twilio")


class NexusHospitalAgent:
    def __init__(self):
        self.deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")

        # Initialize Twilio if available
        if TWILIO_AVAILABLE:
            self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

            if all(
                [
                    self.twilio_account_sid,
                    self.twilio_auth_token,
                    self.twilio_phone_number,
                ]
            ):
                self.twilio_client = Client(
                    self.twilio_account_sid, self.twilio_auth_token
                )
                self.can_make_calls = True
                print("✅ Twilio configured - Outbound calls enabled")
            else:
                self.can_make_calls = False
                print("⚠️  Twilio credentials missing - Only simulated calls available")
        else:
            self.can_make_calls = False

    def sts_connect(self):
        """Connect to Deepgram"""
        sts_ws = websockets.connect(
            uri="wss://agent.deepgram.com/v1/agent/converse",
            extra_headers={"Authorization": f"Token {self.deepgram_api_key}"},
        )
        return sts_ws

    def load_config(self):
        """Load agent configuration"""
        with open("config.json", "r") as f:
            return json.load(f)

    async def make_hospital_call(self, hospital_number, patient_data):
        """Make outbound call to hospital"""
        if not self.can_make_calls:
            return await self.simulate_hospital_call(hospital_number, patient_data)

        try:
            print(f"📞 Making REAL call to {hospital_number}...")

            # Create webhook URL for the call
            ngrok_url = os.getenv("NGROK_URL", "your-ngrok-url.ngrok.io")
            webhook_url = f"https://{ngrok_url}/voice"

            # Make the actual Twilio call
            call = self.twilio_client.calls.create(
                from_=self.twilio_phone_number,
                to=hospital_number,
                url=webhook_url,
                method="POST",
            )

            print(f"✅ Call initiated! SID: {call.sid}")

            return {
                "success": True,
                "call_sid": call.sid,
                "type": "real_call",
                "message": f"Real call to {hospital_number} in progress",
            }

        except Exception as e:
            print(f"❌ Real call failed: {e}")
            print("🔄 Falling back to simulation...")
            return await self.simulate_hospital_call(hospital_number, patient_data)

    async def simulate_hospital_call(self, hospital_number, patient_data):
        """Simulate hospital call with AI conversation"""
        print(f"🎭 SIMULATING call to {hospital_number}")
        print("🤖 This shows how your AI agent will sound...")
        print("=" * 60)

        # Simulate the conversation
        await asyncio.sleep(1)
        print("📞 Ring... Ring... Ring...")
        await asyncio.sleep(2)

        print("👩‍⚕️ Hospital: 'Hello, City General Hospital, how can I help you?'")
        await asyncio.sleep(1)

        print("🤖 Nexus Agent: 'Hello, this is Nexus Health Assistant calling on")
        print("   behalf of a patient who needs to schedule an appointment.")
        print("   May I speak with someone who handles appointment scheduling?'")
        await asyncio.sleep(2)

        print("👩‍⚕️ Hospital: 'Yes, this is Maria in scheduling. How can I help?'")
        await asyncio.sleep(1)

        print(
            f"🤖 Nexus Agent: 'Thank you Maria. I'm calling for {patient_data['name']},"
        )
        print(f"   date of birth {patient_data['dob']}. The patient is experiencing")
        print(
            f"   {patient_data['symptoms']} and needs to see a {patient_data['specialist_type']}."
        )
        print(f"   This is {patient_data['urgency']} priority.'")
        await asyncio.sleep(3)

        print("👩‍⚕️ Hospital: 'I understand. Let me check our availability...")
        print("   We have an opening Thursday at 3:30 PM with Dr. Johnson.'")
        await asyncio.sleep(2)

        print("🤖 Nexus Agent: 'That works well. Could you please confirm:")
        print("   - Date: Thursday, 3:30 PM")
        print("   - Doctor: Dr. Johnson")
        print("   - Department: Cardiology")
        print(f"   The patient has {patient_data['insurance']} insurance and can be")
        print(f"   reached at {patient_data['phone']} if needed.'")
        await asyncio.sleep(2)

        print("👩‍⚕️ Hospital: 'Perfect! Appointment confirmed. Please have the patient")
        print("   arrive 15 minutes early with insurance card and photo ID.'")
        await asyncio.sleep(1)

        print("🤖 Nexus Agent: 'Excellent! Thank you Maria. I'll inform the patient")
        print("   right away. Should they call this number for any changes?'")
        await asyncio.sleep(1)

        print("👩‍⚕️ Hospital: 'Yes, or our main scheduling line. Have a great day!'")
        print("🤖 Nexus Agent: 'Thank you very much. You too!'")

        print("\n✅ APPOINTMENT SUCCESSFULLY BOOKED!")

        return {
            "success": True,
            "type": "simulated_call",
            "appointment": {
                "date": "Thursday, 3:30 PM",
                "doctor": "Dr. Johnson",
                "department": "Cardiology",
                "instructions": "Arrive 15 minutes early with insurance card and ID",
            },
        }

    async def collect_and_call(self):
        """Complete workflow: collect patient info and call hospital"""
        print("=== Nexus Health Assistant - Hospital Calling System ===\n")

        # Collect patient information
        patient_data = {
            "name": input("Patient full name: "),
            "dob": input("Date of birth (MM/DD/YYYY): "),
            "phone": input("Patient phone number: "),
            "email": input("Patient email: "),
            "symptoms": input("Current symptoms: "),
            "specialist_type": input("Specialist needed (e.g., cardiologist): "),
            "urgency": input("Urgency (routine/urgent/same-day): "),
            "insurance": input("Insurance provider: "),
            "preferred_times": input("Preferred appointment times: "),
        }

        hospital_number = input("\nHospital phone number: ")

        # Show summary
        print(f"\n📋 APPOINTMENT REQUEST SUMMARY:")
        print(f"Patient: {patient_data['name']}")
        print(f"Symptoms: {patient_data['symptoms']}")
        print(f"Specialist: {patient_data['specialist_type']}")
        print(f"Urgency: {patient_data['urgency']}")
        print(f"Hospital: {hospital_number}")

        if self.can_make_calls:
            print(f"\n📞 READY TO MAKE REAL CALL")
        else:
            print(f"\n🎭 WILL SIMULATE CALL (Twilio not configured)")

        confirm = input(f"\nProceed? (y/n): ")

        if confirm.lower() != "y":
            print("❌ Cancelled.")
            return

        # Make the call
        result = await self.make_hospital_call(hospital_number, patient_data)

        if result["success"]:
            print(f"\n🎉 SUCCESS!")
            if result["type"] == "real_call":
                print(f"📞 Real call in progress - Call ID: {result['call_sid']}")
                print(f"🤖 Your AI agent is speaking with the hospital now!")
            else:
                print(f"🎭 Call simulation completed successfully")
                print(f"📅 Simulated appointment: {result['appointment']['date']}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")


# Original WebSocket server functionality
async def handle_barge_in(decoded, twilio_ws, streamsid):
    if decoded["type"] == "UserStartedSpeaking":
        clear_message = {"event": "clear", "streamsid": streamsid}
        await twilio_ws.send(json.dumps(clear_message))


async def handle_text_message(decoded, twilio_ws, sts_ws, streamsid):
    await handle_barge_in(decoded, twilio_ws, streamsid)


async def sts_sender(sts_ws, audio_queue):
    print("sts_sender started")
    while True:
        chunk = await audio_queue.get()
        await sts_ws.send(chunk)


async def sts_receiver(sts_ws, twilio_ws, streamsid_queue):
    print("sts_receiver started")
    streamsid = await streamsid_queue.get()

    async for message in sts_ws:
        if type(message) is str:
            decoded = json.loads(message)
            await handle_text_message(decoded, twilio_ws, sts_ws, streamsid)
            continue

        raw_mulaw = message
        media_message = {
            "event": "media",
            "streamsid": streamsid,
            "media": {"payload": base64.b64encode(raw_mulaw).decode("ascii")},
        }

        await twilio_ws.send(json.dumps(media_message))


async def twilio_receiver(twilio_ws, audio_queue, streamsid_queue):
    BUFFER_SIZE = 20 * 160
    inbuffer = bytearray(b"")

    async for message in twilio_ws:
        try:
            data = json.loads(message)
            event = data["event"]

            if event == "start":
                print("get our streamsid")
                start = data["start"]
                streamsid = start["streamsid"]
                streamsid_queue.put_nowait(streamsid)

            elif event == "connected":
                continue

            elif event == "media":
                media = data["media"]
                chunk = base64.b64decode(media["payload"])
                if media["track"] == "inbound":
                    inbuffer.extend(chunk)

            elif event == "stop":
                break

            while len(inbuffer) >= BUFFER_SIZE:
                chunk = inbuffer[:BUFFER_SIZE]
                audio_queue.put_nowait(chunk)
                inbuffer = inbuffer[BUFFER_SIZE:]

        except Exception as e:
            print(f"Error in twilio_receiver: {e}")
            break


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


def sts_connect():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise Exception("DEEPGRAM_API_KEY not found")

    sts_ws = websockets.connect(
        uri="wss://agent.deepgram.com/v1/agent/converse",
        extra_headers={"Authorization": f"Token {api_key}"},
    )
    return sts_ws


async def twilio_handler(twilio_ws):
    audio_queue = asyncio.Queue()
    streamsid_queue = asyncio.Queue()

    async with sts_connect() as sts_ws:
        config_message = load_config()
        await sts_ws.send(json.dumps(config_message))

        await asyncio.gather(
            sts_sender(sts_ws, audio_queue),
            sts_receiver(sts_ws, twilio_ws, streamsid_queue),
            twilio_receiver(twilio_ws, audio_queue, streamsid_queue),
        )

        await twilio_ws.close()


async def main():
    # Check if user wants to make hospital call or start WebSocket server
    mode = input(
        "Choose mode:\n1. Make hospital call\n2. Start WebSocket server\nEnter (1 or 2): "
    )

    if mode == "1":
        # Hospital calling mode
        agent = NexusHospitalAgent()
        await agent.collect_and_call()
    else:
        # WebSocket server mode (original functionality)
        await websockets.serve(twilio_handler, host="localhost", port=5000)
        print("Started WebSocket server on localhost:5000")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
