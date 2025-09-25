"""
Simple Outbound Call Utility for Nexus Health Assistant
Makes outbound calls using Twilio with proper configuration
"""

import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


def make_outbound_call(to_number, message=None):
    """
    Make an outbound call using Twilio
    
    Args:
        to_number (str): Phone number to call (must include country code, e.g., +1234567890)
        message (str, optional): Optional message context for logging
    
    Returns:
        dict: Result with success status and call details
        
    Example:
        result = make_outbound_call("+1234567890", "Calling for appointment booking")
        if result["success"]:
            print(f"Call initiated: {result['call_sid']}")
        else:
            print(f"Call failed: {result['error']}")
    """
    
    # Load Twilio credentials from environment
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    ngrok_url = os.getenv("NGROK_URL")
    
    # Validate environment configuration
    if not all([account_sid, auth_token, from_number, ngrok_url]):
        return {
            "success": False,
            "error": "Missing Twilio configuration. Check TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, and NGROK_URL in .env file"
        }
    
    # Validate phone numbers format
    if not to_number or not to_number.startswith('+'):
        return {
            "success": False,
            "error": "Invalid 'to' phone number. Must include country code (e.g., +1234567890)"
        }
        
    if not from_number.startswith('+'):
        return {
            "success": False,
            "error": "Invalid Twilio phone number format in .env file. Must include country code"
        }
    
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Prepare webhook URL
        webhook_url = ngrok_url.replace('https://', '').replace('http://', '')
        webhook_url = f"https://{webhook_url}/voice"
        
        print(f"🔄 Initiating outbound call...")
        print(f"📞 FROM: {from_number} (Your Twilio Number)")
        print(f"📞 TO: {to_number}")
        if message:
            print(f"📝 Context: {message}")
        print(f"🔗 Webhook: {webhook_url}")
        
        # Make the call
        call = client.calls.create(
            from_=from_number,      # Your Twilio number (source)
            to=to_number,          # Destination number  
            url=webhook_url,       # Your voice webhook endpoint
            method="POST",
            timeout=30            # Ring timeout in seconds
        )
        
        print(f"✅ Call initiated successfully!")
        print(f"🆔 Call SID: {call.sid}")
        print(f"📊 Status: {call.status}")
        
        return {
            "success": True,
            "call_sid": call.sid,
            "status": call.status,
            "from_number": from_number,
            "to_number": to_number,
            "webhook_url": webhook_url,
            "message": f"Call from {from_number} to {to_number} initiated successfully"
        }
        
    except Exception as e:
        error_msg = f"Twilio API Error: {str(e)}"
        print(f"❌ Call failed: {error_msg}")
        
        return {
            "success": False,
            "error": error_msg,
            "from_number": from_number,
            "to_number": to_number
        }


def quick_call(to_number):
    """
    Quick wrapper for making a simple outbound call
    
    Args:
        to_number (str): Phone number to call (with country code)
    
    Returns:
        bool: True if call was initiated successfully, False otherwise
    """
    result = make_outbound_call(to_number)
    return result["success"]


if __name__ == "__main__":
    # Example usage
    print("=== Nexus Health Assistant - Outbound Call Utility ===\n")
    
    # Get phone number from user
    phone = input("Enter phone number to call (with country code, e.g., +1234567890): ")
    
    if not phone:
        print("❌ No phone number provided")
        exit(1)
    
    # Make the call
    result = make_outbound_call(phone, "Test call from Nexus Health Assistant")
    
    if result["success"]:
        print(f"\n🎉 SUCCESS!")
        print(f"Call SID: {result['call_sid']}")
        print(f"The recipient should now be receiving a call from: {result['from_number']}")
    else:
        print(f"\n❌ FAILED: {result['error']}")