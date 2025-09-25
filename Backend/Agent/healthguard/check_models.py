#!/usr/bin/env python3
"""
Check available Groq models
"""

import os
import requests

def check_available_models():
    """Check what models are available in Groq"""
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ No API key found")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers=headers
        )
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Available Groq Models:")
            print("=" * 30)
            
            vision_models = []
            text_models = []
            
            for model in models.get('data', []):
                model_id = model.get('id', '')
                if 'vision' in model_id.lower() or 'llava' in model_id.lower():
                    vision_models.append(model_id)
                else:
                    text_models.append(model_id)
            
            if vision_models:
                print("🔍 Vision Models:")
                for model in vision_models:
                    print(f"   • {model}")
            else:
                print("❌ No vision models found")
            
            print(f"\n💬 Text Models ({len(text_models)}):")
            for model in text_models[:5]:  # Show first 5
                print(f"   • {model}")
            if len(text_models) > 5:
                print(f"   ... and {len(text_models) - 5} more")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_available_models()