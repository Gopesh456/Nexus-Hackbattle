#!/usr/bin/env python3
"""
Setup script to configure GROQ API key for lab analysis
"""

import os
from pathlib import Path

def setup_groq_api_key():
    """Interactive setup for GROQ API key"""
    
    print("🔑 GROQ API Key Setup")
    print("=" * 25)
    
    # Check if API key is already set
    current_key = os.getenv('GROQ_API_KEY')
    if current_key:
        print(f"✅ GROQ_API_KEY is already set (ends with: ...{current_key[-4:]})")
        use_existing = input("Do you want to use the existing key? (y/n): ").lower().strip()
        if use_existing == 'y':
            return current_key
    
    print("\n📝 Please enter your GROQ API key:")
    print("   (You can get one from: https://console.groq.com/keys)")
    
    api_key = input("GROQ_API_KEY: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return None
    
    # Validate API key format (basic check)
    if not api_key.startswith('gsk_'):
        print("⚠️  Warning: GROQ API keys usually start with 'gsk_'")
        continue_anyway = input("Continue anyway? (y/n): ").lower().strip()
        if continue_anyway != 'y':
            return None
    
    # Create .env file
    env_file = Path(".env")
    
    # Read existing .env content
    existing_content = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            existing_content = f.readlines()
    
    # Remove any existing GROQ_API_KEY lines
    new_content = [line for line in existing_content if not line.startswith('GROQ_API_KEY=')]
    
    # Add the new API key
    new_content.append(f'GROQ_API_KEY={api_key}\n')
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        f.writelines(new_content)
    
    # Also set for current session
    os.environ['GROQ_API_KEY'] = api_key
    
    print(f"✅ API key saved to .env file and set for current session")
    print(f"   Key ends with: ...{api_key[-4:]}")
    
    return api_key

if __name__ == "__main__":
    api_key = setup_groq_api_key()
    if api_key:
        print("\n🎉 API key setup complete!")
        print("   You can now run the lab analysis script.")
    else:
        print("\n❌ API key setup failed.")