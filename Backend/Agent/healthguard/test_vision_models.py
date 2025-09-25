#!/usr/bin/env python3
"""
Test multiple Groq vision model names
"""

import os
import base64
import requests
from pathlib import Path

def test_vision_models():
    """Test different vision model names"""
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ No API key")
        return
    
    # Different model names to try
    models_to_try = [
        "llama-3.2-90b-vision-preview",
        "llama-3.2-11b-vision-preview", 
        "llava-v1.5-7b-4096-preview",
        "llama3.2-11b-vision-preview",
        "llama3.2-90b-vision-preview",
        "llava-1.5-7b-hf",
        "llava-v1.6-34b",
        "llama-vision-3.2-11b",
        "llama-vision-3.2-90b"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Simple text-only test first
    print("🔍 Testing Groq Vision Models...")
    print("=" * 35)
    
    for model in models_to_try:
        print(f"Testing: {model}")
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, can you analyze images?"
                }
            ],
            "max_tokens": 50
        }
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"  ✅ {model} - WORKS!")
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"     Response: {content[:50]}...")
                return model  # Return the working model
            else:
                error = response.json().get('error', {})
                if 'decommissioned' in error.get('message', ''):
                    print(f"  ❌ {model} - Decommissioned")
                elif 'not found' in error.get('message', ''):
                    print(f"  ❌ {model} - Not found")
                else:
                    print(f"  ❌ {model} - Error: {response.status_code}")
                    
        except Exception as e:
            print(f"  ❌ {model} - Exception: {str(e)[:30]}...")
    
    print("\n❌ No working vision models found")
    return None

if __name__ == "__main__":
    working_model = test_vision_models()
    if working_model:
        print(f"\n🎉 Found working model: {working_model}")
    else:
        print("\n😞 All vision models seem to be unavailable")
        print("Consider using OpenAI GPT-4 Vision instead")