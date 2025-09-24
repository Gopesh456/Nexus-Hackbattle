# Nexus Health Assistant - Hospital Appointment Booking System

## Overview

This system allows the Nexus AI voice agent to make outbound calls to hospitals and book appointments on behalf of patients. The AI agent professionally communicates with hospital staff, presents patient information, and schedules appointments.

## Architecture

```
Patient → Nexus Interface → AI Agent → Hospital Call → Appointment Booked
```

## Files Structure

- `main_outbound.py` - Main outbound calling system with Twilio integration
- `config.json` - AI agent configuration for hospital communications
- `book_appointment.py` - Simple interface to trigger hospital calls
- `.env` - Environment variables for API keys

## Setup Instructions

### 1. Install Dependencies

```bash
uv add websockets python-dotenv twilio flask
```

### 2. Configure Environment Variables

Update `.env` file with your credentials:

```
DEEPGRAM_API_KEY='your_deepgram_api_key'
TWILIO_ACCOUNT_SID='your_twilio_account_sid'
TWILIO_AUTH_TOKEN='your_twilio_auth_token'
TWILIO_PHONE_NUMBER='your_twilio_phone_number'
NGROK_URL='your-ngrok-url.ngrok.io'
```

### 3. Set Up Ngrok (for webhooks)

```bash
ngrok http 5001
```

Update `NGROK_URL` in `.env` with your ngrok URL.

### 4. Configure Twilio Webhooks

In your Twilio Console, set webhook URLs:

- Voice URL: `https://your-ngrok-url.ngrok.io/patient-call`
- Outbound calls: `https://your-ngrok-url.ngrok.io/hospital-call`

## How It Works

### Patient Information Collection

The AI agent collects:

- Full name and date of birth
- Contact information (phone, email)
- Current symptoms and medical concerns
- Insurance provider information
- Preferred appointment times
- Specialist type needed
- Urgency level (routine/urgent/same-day)

### Hospital Communication Protocol

When calling hospitals, the AI agent:

1. **Professional Introduction**:
   "Hello, this is Nexus Health Assistant calling on behalf of a patient who needs to schedule an appointment."

2. **Patient Information Presentation**:
   "I'm calling for [Patient Name], date of birth [DOB]. The patient is experiencing [symptoms] and needs to see [specialist type]."

3. **Appointment Request**:
   "Could you please check availability for [preferred timeframe]? The patient has [insurance provider] insurance."

4. **Details Confirmation**:
   Confirms appointment date, time, location, doctor name, and preparation requirements.

5. **Follow-up Information**:
   Provides patient contact details and reschedule procedures.

## Usage

### Method 1: Simple Booking Interface

```bash
python book_appointment.py
```

This will prompt for patient information and trigger the hospital call.

### Method 2: API Integration

Send POST request to `/book-appointment` endpoint:

```json
{
  "name": "John Doe",
  "dob": "01/15/1980",
  "phone": "+1234567890",
  "email": "john@email.com",
  "symptoms": "chest pain, shortness of breath",
  "specialist_type": "cardiologist",
  "urgency": "urgent",
  "insurance": "Blue Cross Blue Shield",
  "preferred_times": "Monday-Wednesday mornings",
  "hospital_number": "+1555123456"
}
```

### Method 3: Full System (WebSocket + Flask)

```bash
python main_outbound.py
```

This runs both the WebSocket server (port 5000) and Flask API (port 5001).

## AI Agent Features

### Professional Communication

- Uses medical terminology appropriately
- Maintains professional tone with hospital staff
- Respects staff time and procedures
- Handles transfers between departments

### HIPAA Compliance

- Only shares necessary appointment scheduling information
- Maintains patient confidentiality
- Secure data transmission

### Emergency Protocols

- Recognizes emergency symptoms
- Escalates to emergency services when needed
- Requests same-day appointments for urgent cases

### Conversation Management

- Handles interruptions and clarifications
- Repeats information when requested
- Confirms all details before ending calls
- Provides clear next steps

## Testing

### Test Hospital Call Flow

1. Run the booking system
2. Enter test patient information
3. Use a test phone number (your own) as "hospital number"
4. Observe the AI agent's professional communication

### Emergency Scenarios

Test with urgent symptoms:

- "chest pain and difficulty breathing" → Same-day cardiology
- "severe headache and vision changes" → Urgent neurology
- "high fever in elderly patient" → Same-day primary care

## Integration with Existing System

This hospital calling system integrates with your existing Nexus health monitoring:

1. **Anomaly Detection** → Triggers appointment booking
2. **Voice Agent** → Collects patient info and calls hospitals
3. **Django Backend** → Stores appointment confirmations
4. **Frontend** → Displays booking status and confirmations

## Security Considerations

- All API keys stored in environment variables
- HTTPS required for webhook endpoints
- Patient data encrypted in transit
- HIPAA-compliant data handling
- No persistent storage of sensitive information

## Troubleshooting

### Common Issues

1. **Ngrok URL expired**: Update `.env` with new ngrok URL
2. **Twilio webhooks not working**: Check ngrok is running and URLs are correct
3. **Deepgram connection failed**: Verify API key is valid
4. **Call not connecting**: Check Twilio phone number and permissions

### Logs and Debugging

- WebSocket server logs show connection status
- Twilio Console shows call logs and webhook delivery
- Deepgram logs show conversation transcripts

## Next Steps

1. **Integration Testing**: Test with real hospital numbers (with permission)
2. **Database Integration**: Store appointment confirmations
3. **Patient Notifications**: SMS/email confirmations
4. **Advanced Features**: Multi-language support, insurance verification
5. **Analytics**: Track booking success rates and call durations

---

**Important**: Always obtain proper consent from patients before making calls on their behalf, and ensure compliance with healthcare regulations in your jurisdiction.
