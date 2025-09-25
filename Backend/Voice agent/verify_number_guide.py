"""
Twilio Trial Account Helper - Phone Number Verification Guide
"""


def show_verification_steps():
    print("🔐 TWILIO TRIAL ACCOUNT DETECTED")
    print("=" * 50)
    print()
    print("❌ Cannot call +917306598211 - Number not verified")
    print()
    print("📋 TO VERIFY THE NUMBER:")
    print(
        "1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified"
    )
    print("2. Click 'Add a new number'")
    print("3. Enter: +917306598211")
    print("4. Choose verification method (SMS or Voice)")
    print("5. Enter the verification code sent to that number")
    print()
    print("✅ AFTER VERIFICATION:")
    print("- The number will be added to your verified list")
    print("- You can then make calls to +917306598211")
    print("- Trial accounts can call verified numbers for free")
    print()
    print("🚀 ALTERNATIVE SOLUTIONS:")
    print("1. Upgrade to paid Twilio account ($0.85/call to India)")
    print("2. Test with a US/Canada number (often work on trial)")
    print("3. Use your own verified phone number for testing")
    print()
    print("💡 TIP: You can verify up to 10 numbers on trial account")


def test_different_number():
    """Test with a US number that might work on trial account"""
    print()
    print("🧪 TESTING WITH US NUMBER...")

    # This might work on trial account
    test_number = "+15551234567"  # This is often a test number

    try:
        from outbound_call_utility import make_outbound_call

        result = make_outbound_call(test_number, "US test call")

        if result["success"]:
            print("✅ US number test successful!")
        else:
            print(f"❌ US number test failed: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error testing US number: {e}")


if __name__ == "__main__":
    show_verification_steps()

    # Ask if user wants to test US number
    try_us = input("\nTest with US number? (y/n): ")
    if try_us.lower() == "y":
        test_different_number()
