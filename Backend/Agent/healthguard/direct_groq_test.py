#!/usr/bin/env python3
"""
Direct Groq API test for lab report analysis
"""

import os
import base64
import json
import requests
from pathlib import Path

def analyze_lab_report():
    """Analyze lab report using Groq vision API"""
    
    print("🏥 Groq Vision Lab Report Analysis")
    print("=" * 35)
    
    # Check API key
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found")
        return
    
    print(f"✅ API Key ready (ends with: ...{api_key[-4:]})")
    
    # Find lab report image
    image_path = Path("../images/WhatsApp Image 2025-09-25 at 03.06.20.jpeg")
    if not image_path.exists():
        print(f"❌ Lab report image not found: {image_path}")
        return
    
    print(f"📸 Found lab report: {image_path.name}")
    
    # Convert image to base64
    try:
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        print(f"✅ Converted to base64 ({len(image_data)} characters)")
    except Exception as e:
        print(f"❌ Failed to convert image: {e}")
        return
    
    # Prepare Groq API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.2-11b-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": """You are an expert medical AI assistant specializing in lab report analysis. 
                
Analyze the provided lab report image and extract ALL medical information with high accuracy.

Focus on extracting:
1. Patient demographics (name, age, gender, ID)
2. Lab facility information (name, address, phone)
3. Report details (ID, dates, doctor name)
4. All test parameters with exact values and units
5. Reference ranges for each parameter
6. Abnormal values and their clinical significance

Provide comprehensive medical insights and return a structured JSON response."""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Please analyze this lab report image and extract all medical data.

Return a comprehensive JSON response with:
- Patient information (name, age, gender, ID)
- Lab details (name, address, report ID, dates)
- All test results with values, units, and reference ranges
- Identification of abnormal/critical values
- Clinical interpretation and health insights
- Recommendations for follow-up care

Be thorough and accurate in your extraction."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4000,
        "temperature": 0.1
    }
    
    print("🚀 Sending to Groq Vision AI...")
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_content = result['choices'][0]['message']['content']
            usage = result.get('usage', {})
            
            print("✅ SUCCESS! Lab Report Analysis Complete!")
            print("=" * 50)
            print(ai_content)
            print("=" * 50)
            
            # Save the analysis
            timestamp = "20250925"
            analysis_file = f"lab_analysis_{timestamp}.json"
            
            with open(analysis_file, 'w') as f:
                json.dump({
                    "image_analyzed": str(image_path),
                    "groq_model": "llava-v1.5-7b-4096-preview",
                    "analysis_content": ai_content,
                    "usage_stats": usage,
                    "raw_response": result
                }, f, indent=2)
            
            print(f"💾 Analysis saved to: {analysis_file}")
            
            # Show API usage stats
            print(f"\n📊 API Usage Statistics:")
            print(f"   Total Tokens: {usage.get('total_tokens', 'N/A')}")
            print(f"   Prompt Tokens: {usage.get('prompt_tokens', 'N/A')}")
            print(f"   Completion Tokens: {usage.get('completion_tokens', 'N/A')}")
            print(f"   Model Used: {result.get('model', 'N/A')}")
            
            return ai_content
            
        else:
            print(f"❌ Groq API Error: {response.status_code}")
            print(f"Error Response: {response.text}")
            
            if response.status_code == 401:
                print("🔑 Check your GROQ_API_KEY - it might be invalid")
            elif response.status_code == 429:
                print("⏰ Rate limit exceeded - try again in a moment")
                
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - the image might be too large")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

if __name__ == "__main__":
    result = analyze_lab_report()
    if result:
        print("\n🎉 Lab report successfully analyzed by Groq AI!")
    else:
        print("\n😞 Analysis failed - check the errors above")