import asyncio
import base64
import json
import websockets
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml import VoiceResponse
from flask import Flask, request
import threading
from dataclasses import dataclass
from typing import Optional

load_dotenv()


@dataclass
class PatientInfo:
    name: str
    dob: str
    phone: str
    email: str
    symptoms: str
    specialist_type: str
    urgency: str
    insurance: str
    preferred_times: str


app = Flask(__name__)


class NexusHealthAgent:
    def __init__(self):
        self.deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

        if not all(
            [
                self.deepgram_api_key,
                self.twilio_account_sid,
                self.twilio_auth_token,
                self.twilio_phone_number,
            ]
        ):
            raise Exception("Missing required environment variables")

        self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        self.patient_sessions = {}

    def load_config(self):
        with open("config.json", "r") as f:
            return json.load(f)

    async def collect_patient_information(self, websocket):
        """Collect patient information through voice interaction"""
        patient_info = PatientInfo(
            name="",
            dob="",
            phone="",
            email="",
            symptoms="",
            specialist_type="",
            urgency="",
            insurance="",
            preferred_times="",
        )

        # This would be handled through the Deepgram conversation
        # The AI agent will collect this information step by step
        return patient_info

    async def make_hospital_call(self, patient_info: PatientInfo, hospital_number: str):
        """Make outbound call to hospital for appointment booking"""
        try:
            # Create TwiML for the outbound call
            call = self.twilio_client.calls.create(
                url=f"http://{os.getenv('NGROK_URL', 'your-ngrok-url.ngrok.io')}/hospital-call",
                to=hospital_number,
                from_=self.twilio_phone_number,
                method="POST",
            )

            print(f"Making call to {hospital_number} with Call SID: {call.sid}")
            return call.sid

        except Exception as e:
            print(f"Error making hospital call: {e}")
            return None

    def sts_connect(self):
        """Connect to Deepgram Speech-to-Speech service"""
        sts_ws = websockets.connect(
            uri="wss://agent.deepgram.com/v1/agent/converse",
            extra_headers={"Authorization": f"Token {self.deepgram_api_key}"},
        )
        return sts_ws

    async def handle_patient_session(self, websocket):
        """Handle incoming patient calls to collect information"""
        session_id = id(websocket)
        self.patient_sessions[session_id] = {
            "stage": "collecting_info",
            "patient_info": None,
            "hospital_numbers": [],
        }

        try:
            async with self.sts_connect() as sts_ws:
                config_message = self.load_config()
                await sts_ws.send(json.dumps(config_message))

                # Handle the patient information collection session
                await self.handle_deepgram_session(websocket, sts_ws, session_id)

        except Exception as e:
            print(f"Error in patient session: {e}")
        finally:
            if session_id in self.patient_sessions:
                del self.patient_sessions[session_id]

    async def handle_deepgram_session(self, twilio_ws, sts_ws, session_id):
        """Handle the Deepgram conversation session"""
        audio_queue = asyncio.Queue()
        streamsid_queue = asyncio.Queue()

        await asyncio.gather(
            self.sts_sender(sts_ws, audio_queue),
            self.sts_receiver(sts_ws, twilio_ws, streamsid_queue),
            self.twilio_receiver(twilio_ws, audio_queue, streamsid_queue, session_id),
        )

    async def sts_sender(self, sts_ws, audio_queue):
        """Send audio to Deepgram"""
        print("sts_sender started")
        while True:
            chunk = await audio_queue.get()
            await sts_ws.send(chunk)

    async def sts_receiver(self, sts_ws, twilio_ws, streamsid_queue):
        """Receive responses from Deepgram"""
        print("sts_receiver started")
        streamsid = await streamsid_queue.get()

        async for message in sts_ws:
            if isinstance(message, str):
                decoded = json.loads(message)
                await self.handle_text_message(decoded, twilio_ws, sts_ws, streamsid)
                continue

            raw_mulaw = message
            media_message = {
                "event": "media",
                "streamSid": streamsid,
                "media": {"payload": base64.b64encode(raw_mulaw).decode("ascii")},
            }

            await twilio_ws.send(json.dumps(media_message))

    async def twilio_receiver(
        self, twilio_ws, audio_queue, streamsid_queue, session_id
    ):
        """Receive audio from Twilio"""
        BUFFER_SIZE = 20 * 160
        inbuffer = bytearray(b"")

        async for message in twilio_ws:
            try:
                data = json.loads(message)
                event = data["event"]

                if event == "start":
                    print("Session started")
                    start = data["start"]
                    streamsid = start["streamSid"]
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

    async def handle_text_message(self, decoded, twilio_ws, sts_ws, streamsid):
        """Handle text messages from Deepgram (for barge-in, etc.)"""
        if decoded.get("type") == "UserStartedSpeaking":
            clear_message = {"event": "clear", "streamSid": streamsid}
            await twilio_ws.send(json.dumps(clear_message))


# Flask routes for Twilio webhooks
nexus_agent = NexusHealthAgent()


@app.route("/patient-call", methods=["POST"])
def handle_patient_call():
    """Handle incoming patient calls"""
    response = VoiceResponse()
    response.start_stream(url=f"wss://your-websocket-server.ngrok.io/patient-session")
    return str(response)


@app.route("/hospital-call", methods=["POST"])
def handle_hospital_call():
    """Handle outbound calls to hospitals"""
    response = VoiceResponse()

    # This will connect the hospital call to Deepgram for AI conversation
    response.start_stream(url=f"wss://your-websocket-server.ngrok.io/hospital-session")
    return str(response)


@app.route("/book-appointment", methods=["POST"])
def book_appointment():
    """API endpoint to trigger hospital calls"""
    data = request.json

    patient_info = PatientInfo(
        name=data.get("name"),
        dob=data.get("dob"),
        phone=data.get("phone"),
        email=data.get("email"),
        symptoms=data.get("symptoms"),
        specialist_type=data.get("specialist_type"),
        urgency=data.get("urgency"),
        insurance=data.get("insurance"),
        preferred_times=data.get("preferred_times"),
    )

    hospital_number = data.get("hospital_number")

    # Make the hospital call
    call_sid = asyncio.run(
        nexus_agent.make_hospital_call(patient_info, hospital_number)
    )

    return json.dumps({"status": "success", "call_sid": call_sid})


async def start_websocket_server():
    """Start the WebSocket server for handling Twilio streams"""
    print("Starting WebSocket server on localhost:5000")
    await websockets.serve(nexus_agent.handle_patient_session, "localhost", 5000)
    print("WebSocket server started")


def run_flask_app():
    """Run Flask app for Twilio webhooks"""
    print("Starting Flask app on port 5001")
    app.run(host="0.0.0.0", port=5001, debug=False)


async def main():
    """Main function to run both servers"""
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()

    # Start WebSocket server
    await start_websocket_server()

    # Keep the program running
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
