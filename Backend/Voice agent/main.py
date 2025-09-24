import asyncio
import def load_config():
    with open("config.json","r") as f:
        return json.load(f)

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
        "insurance": input("Insurance: ")
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
            if confirm.lower() == 'y':
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
            url="http://demo.twilio.com/docs/voice.xml"  # Simple test TwiML
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
    print(f"   on behalf of {patient_data['name']} who needs to schedule an appointment.")
    print(f"   May I speak with someone in scheduling?'")
    
    print(f"\n👩‍⚕️ Hospital: 'Yes, this is scheduling. How can I help?'")
    
    print(f"\n🤖 Nexus Agent: 'I'm calling for {patient_data['name']}, DOB {patient_data['dob']}.")
    print(f"   The patient is experiencing {patient_data['symptoms']} and needs to see")
    print(f"   a {patient_data['specialist']}. This is {patient_data['urgency']} priority.'")
    
    print(f"\n👩‍⚕️ Hospital: 'I can schedule that. We have availability Tuesday at 2 PM")
    print(f"   with Dr. Martinez.'")
    
    print(f"\n🤖 Nexus Agent: 'Perfect! Could you confirm: Tuesday 2 PM with Dr. Martinez?")
    print(f"   The patient has {patient_data['insurance']} insurance and can be reached")
    print(f"   at {patient_data['phone']}.'")
    
    print(f"\n👩‍⚕️ Hospital: 'Confirmed! Please arrive 15 minutes early.'")
    
    print(f"\n🤖 Nexus Agent: 'Thank you! I'll inform the patient immediately.'")
    
    print(f"\n✅ APPOINTMENT BOOKED!")
    print(f"📅 Tuesday 2 PM with Dr. Martinez")
    
    return {"success": True, "type": "simulation", "appointment": "Tuesday 2 PM"}e64
import json
import websockets
import os
from dotenv import load_dotenv

load_dotenv()


def sts_connect():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise Exception("DEEPGRAM_API_KEY not found")

    sts_ws = websockets.connect(
        uri="wss://agent.deepgram.com/v1/agent/converse",
        extra_headers={"Authorization": f"Token {api_key}"},
    )

    return sts_ws


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


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

        except:
            break


async def twilio_handler(twilio_ws):
    audio_queue = asyncio.Queue()
    streamsid_queue = asyncio.Queue()

    async with sts_connect() as sts_ws:
        config_message = load_config()
        await sts_ws.send(json.dumps(config_message))

        await asyncio.wait(
            [
                asyncio.ensure_future(sts_sender(sts_ws, audio_queue)),
                asyncio.ensure_future(sts_receiver(sts_ws, twilio_ws, streamsid_queue)),
                asyncio.ensure_future(
                    twilio_receiver(twilio_ws, audio_queue, streamsid_queue)
                ),
            ]
        )

        await twilio_ws.close()


async def main():
    await websockets.serve(twilio_handler, host="localhost", port=5000)
    print("Started server")
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
