"""
Test script for validating Twilio outbound call configuration
This script tests the configuration without making actual calls
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_twilio_configuration():
    """Test that Twilio is properly configured for outbound calls"""
    
    print("=== Nexus Health Assistant - Twilio Configuration Test ===\n")
    
    # Check environment variables
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN") 
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    ngrok_url = os.getenv("NGROK_URL")
    
    print("🔍 Environment Variables Check:")
    print(f"  TWILIO_ACCOUNT_SID: {'✅ Set' if account_sid else '❌ Missing'}")
    print(f"  TWILIO_AUTH_TOKEN: {'✅ Set' if auth_token else '❌ Missing'}")
    print(f"  TWILIO_PHONE_NUMBER: {'✅ Set' if from_number else '❌ Missing'}")
    print(f"  NGROK_URL: {'✅ Set' if ngrok_url else '❌ Missing'}")
    
    if not all([account_sid, auth_token, from_number, ngrok_url]):
        print("\n❌ Configuration incomplete. Please check your .env file.")
        return False
    
    print(f"\n📞 Outbound Call Configuration:")
    print(f"  FROM Number (Your Twilio): {from_number}")
    print(f"  Account SID: {account_sid[:8]}...")
    print(f"  Webhook Base URL: {ngrok_url}")
    
    # Validate phone number format
    if not from_number.startswith('+'):
        print(f"\n⚠️  Warning: Twilio phone number should start with '+' (country code)")
        return False
        
    # Test webhook URL format
    if ngrok_url:
        webhook_test = ngrok_url.replace('https://', '').replace('http://', '')
        webhook_url = f"https://{webhook_test}/voice"
        print(f"  Full Webhook URL: {webhook_url}")
    
    print(f"\n✅ Configuration appears valid!")
    print(f"\n📋 How outbound calls will work:")
    print(f"  • FROM: {from_number} (Your Twilio number)")
    print(f"  • TO: [Phone number you provide]")
    print(f"  • Webhook: {webhook_url}")
    print(f"  • The recipient will see a call from: {from_number}")
    
    return True

def test_call_format(test_number):
    """Test if a phone number is in the correct format"""
    print(f"\n🧪 Testing phone number format: {test_number}")
    
    if not test_number:
        print("❌ Empty phone number")
        return False
        
    if not test_number.startswith('+'):
        print("❌ Phone number must start with '+' (country code)")
        return False
        
    if len(test_number) < 10:
        print("❌ Phone number too short")
        return False
        
    print("✅ Phone number format looks valid")
    return True

if __name__ == "__main__":
    # Test configuration
    config_ok = test_twilio_configuration()
    
    if config_ok:
        print(f"\n" + "="*50)
        print("🧪 Test a phone number format:")
        
        # Test some example numbers
        test_numbers = [
            "+17603886088",  # Your Twilio number
            "+918015610837", # Indian number (needs verification)
            "+1234567890",   # Valid US format
            "1234567890",    # Missing country code
            "+44123456789"   # Valid UK format
        ]
        
        for num in test_numbers:
            test_call_format(num)
            
        print(f"\n" + "="*50)
        print("💡 To make an outbound call:")
        print("   1. Use outbound_call_utility.py")
        print("   2. Or call the API: POST /book-appointment")
        print("   3. Always use full international format: +[country][number]")
        print(f"   4. Calls will appear to come from: {os.getenv('TWILIO_PHONE_NUMBER')}")
    else:
        print("\n❌ Please fix the configuration issues above before making calls.")