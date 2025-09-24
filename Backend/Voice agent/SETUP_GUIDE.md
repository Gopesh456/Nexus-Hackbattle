# 🚀 Nexus Hospital Calling - Complete Setup Guide

## 📋 What You've Got Now

Your system can now make **REAL phone calls** to hospitals! Here's what I've created:

### ✅ New Files Created:

- `main_enhanced.py` - Complete hospital calling system with real calls + simulation
- `real_hospital_caller.py` - Simple hospital calling interface
- `webhook_server.py` - Flask server for Twilio webhooks

### ✅ Enhanced Files:

- `.env` - Added Twilio configuration placeholders
- `config.json` - Already configured with hospital communication prompts

## 🔧 Setup Steps to Make REAL Calls

### Step 1: Install Twilio

```bash
cd "Backend\Voice agent"
uv add twilio flask
```

### Step 2: Get Twilio Account

1. Go to https://www.twilio.com/try-twilio
2. Sign up for free account ($15 credit)
3. Get your credentials from Twilio Console:
   - Account SID (starts with AC...)
   - Auth Token
   - Buy a phone number for outbound calls

### Step 3: Update .env File

Replace the placeholders in your `.env` file:

```env
DEEPGRAM_API_KEY='d53caa236eb1e89709840448f5bf07a3f1ae2321'

# Add your real Twilio credentials here:
TWILIO_ACCOUNT_SID='AC1234567890abcdef1234567890abcdef'
TWILIO_AUTH_TOKEN='your_auth_token_here'
TWILIO_PHONE_NUMBER='+15551234567'

# Set up ngrok for webhooks:
NGROK_URL='abc123.ngrok.io'
```

### Step 4: Set up Ngrok (for webhooks)

1. Download from https://ngrok.com
2. Run: `ngrok http 5001`
3. Copy the https URL (like abc123.ngrok.io)
4. Update NGROK_URL in .env file

### Step 5: Start the Systems

```bash
# Terminal 1: Start webhook server
python webhook_server.py

# Terminal 2: Make hospital calls
python main_enhanced.py
```

## 🧪 Testing Options

### Option 1: Test with Simulation (Works Now!)

```bash
python main_enhanced.py
# Choose option 1 (Make hospital call)
# Enter any phone number - it will simulate the call
```

### Option 2: Test with Your Own Phone

Once Twilio is set up:

```bash
python main_enhanced.py
# Enter YOUR phone number as "hospital number"
# The AI will actually call you!
```

### Option 3: Real Hospital Call

⚠️ **Only after testing with your own number first!**

## 🎯 What Happens During Real Calls

1. **Patient enters information** (symptoms, insurance, etc.)
2. **System dials hospital** using Twilio
3. **AI agent speaks** when hospital answers:

   > "Hello, this is Nexus Health Assistant calling on behalf of a patient who needs to schedule an appointment..."

4. **AI provides patient details**:

   - Name and date of birth
   - Current symptoms
   - Specialist needed
   - Insurance information
   - Urgency level

5. **AI books appointment** and confirms all details

## 📞 Example Real Conversation

```
🤖: "Hello, this is Nexus Health Assistant calling on behalf
     of John Smith, date of birth 01/15/1990..."

👩‍⚕️: "Hi, this is scheduling. How can I help?"

🤖: "The patient is experiencing chest pain and shortness of
     breath and needs to see a cardiologist urgently..."

👩‍⚕️: "Let me check... we have Thursday at 2 PM available."

🤖: "Perfect! Could you confirm: Thursday 2 PM with which doctor?"
```

## ⚠️ Important Safety Notes

1. **Test with YOUR phone first** - Don't call hospitals without permission
2. **Use Twilio test credentials** initially
3. **Comply with regulations** - calling medical facilities may have legal requirements
4. **Get consent** from patients before making calls on their behalf

## 🚀 Ready to Test!

Try this command right now (works without Twilio setup):

```bash
python main_enhanced.py
```

Choose option 1 and see your AI agent in action! It will simulate a complete hospital conversation showing exactly how it will sound during real calls.

Your Nexus Health Assistant is ready to book appointments! 🏥📞🤖
