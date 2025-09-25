#!/usr/bin/env python3
"""
Test the llama-4-scout model (text-only)
"""

import os
import requests

def test_llama_scout():
    """Test the llama-4-scout model"""
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ No API key")
        return
    
    print("🦙 Testing meta-llama/llama-4-scout-17b-16e-instruct")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test with a simple text request first
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "user",
                "content": "Hello! Can you help analyze medical lab reports if I provide the text data?"
            }
        ],
        "max_tokens": 200,
        "temperature": 0.1
    }
    
    try:
        print("🚀 Testing basic text functionality...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            usage = result.get('usage', {})
            
            print("✅ SUCCESS! Model is working!")
            print("=" * 30)
            print(content)
            print("=" * 30)
            print(f"📊 Usage: {usage.get('total_tokens', 'N/A')} tokens")
            
            # Now test if it can handle image analysis instructions
            print("\n🔬 Testing medical analysis capabilities...")
            
            medical_payload = {
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert medical AI assistant specializing in lab report analysis. You help extract and interpret medical data from lab reports."
                    },
                    {
                        "role": "user",
                        "content": """If I provide you with extracted text from a lab report image (using OCR), can you:
1. Identify all lab parameters and their values
2. Determine which values are abnormal
3. Provide clinical interpretations
4. Format the results in JSON structure

For example, if I give you OCR text from a blood test, can you extract Hemoglobin: 12.5 g/dL, identify if it's normal/abnormal, and explain what it means?"""
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.1
            }
            
            med_response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=medical_payload,
                timeout=30
            )
            
            if med_response.status_code == 200:
                med_result = med_response.json()
                med_content = med_result['choices'][0]['message']['content']
                
                print("✅ Medical Analysis Capability:")
                print("=" * 35)
                print(med_content)
                print("=" * 35)
                
                return True
            else:
                print(f"❌ Medical test failed: {med_response.status_code}")
                return False
                
        else:
            print(f"❌ Model test failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        return False

if __name__ == "__main__":
    success = test_llama_scout()
    if success:
        print("\n🎉 Great! This model can help with lab report analysis!")
        print("\n💡 Hybrid Approach:")
        print("1. Use OCR to extract text from lab images")
        print("2. Send extracted text to llama-4-scout for analysis")
        print("3. Get structured medical insights")
    else:
        print("\n😞 Model not suitable for our needs")