from flask import Flask, request
from twilio.twiml import VoiceResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/voice", methods=["POST"])
def handle_voice_call():
    """Handle incoming voice call and connect to Deepgram WebSocket"""
    response = VoiceResponse()

    # Get the WebSocket URL for your Deepgram agent
    websocket_url = f"wss://{os.getenv('NGROK_URL', 'localhost:5000')}/stream"

    # Connect the call to your WebSocket server
    connect = response.connect()
    connect.stream(url=websocket_url)

    return str(response)


@app.route("/stream", methods=["POST"])
def handle_stream():
    """Handle WebSocket stream events"""
    # This would handle the WebSocket events
    return "OK"


if __name__ == "__main__":
    print("🌐 Starting Twilio webhook server...")
    print("📞 Voice calls will be handled at /voice endpoint")
    print("🔗 Make sure to update your ngrok URL in .env file")
    app.run(host="0.0.0.0", port=5001, debug=True)
