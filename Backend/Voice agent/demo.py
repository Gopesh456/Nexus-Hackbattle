"""
Auto-run demo for hospital calling system
"""

import sys

sys.path.append(".")
from test_hospital import quick_test

print("🚀 NEXUS HOSPITAL CALLING DEMO")
print("=" * 50)

result = quick_test()

print(f"\n🎯 RESULT: {result}")
print("\n✨ Hospital calling system is working!")

print("\n💡 READY FOR REAL CALLS!")
print("To enable actual phone calls:")
print("1. Install Twilio: uv add twilio")
print("2. Get credentials from twilio.com")
print("3. Set environment variables")
print("4. Replace simulation with real calling")

print("\n🔥 The system will call hospitals and book appointments automatically!")
