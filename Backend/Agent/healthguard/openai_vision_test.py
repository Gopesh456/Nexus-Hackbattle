#!/usr/bin/env python3
"""
OpenAI GPT-4 Vision integration for lab report analysis
"""

import os
import base64
import json
import requests
from pathlib import Path

def analyze_with_openai():
    """Analyze lab report using OpenAI GPT-4 Vision"""
    
    print("🏥 OpenAI GPT-4 Vision Lab Analysis")
    print("=" * 35)
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        print("Get your API key from: https://platform.openai.com/api-keys")
        print("Then set it: $env:OPENAI_API_KEY='your-key-here'")
        return
    
    print(f"✅ OpenAI API Key ready")
    
    # Find lab report image
    image_path = Path("../images/WhatsApp Image 2025-09-25 at 03.06.20.jpeg")
    if not image_path.exists():
        print(f"❌ Lab report image not found: {image_path}")
        return
    
    print(f"📸 Found lab report: {image_path.name}")
    
    # Convert image to base64
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    print(f"✅ Converted to base64 ({len(image_data)} characters)")
    
    # Prepare OpenAI API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",  # Latest GPT-4 with vision
        "messages": [
            {
                "role": "system",
                "content": """You are an expert medical AI assistant specializing in lab report analysis. 

Analyze the provided lab report image and extract ALL medical information with high accuracy.

Return your analysis in this exact JSON format:
{
  "patient_info": {
    "name": "extracted_name",
    "age": "extracted_age", 
    "gender": "extracted_gender",
    "patient_id": "extracted_id"
  },
  "lab_info": {
    "lab_name": "extracted_lab_name",
    "report_id": "extracted_report_id",
    "test_date": "extracted_date",
    "report_date": "extracted_date"
  },
  "test_results": [
    {
      "parameter": "parameter_name",
      "value": "numeric_value",
      "unit": "measurement_unit", 
      "reference_range": "normal_range",
      "status": "normal/abnormal/critical"
    }
  ],
  "abnormal_findings": [
    {
      "parameter": "parameter_name",
      "value": "current_value",
      "normal_range": "expected_range",
      "clinical_significance": "explanation"
    }
  ],
  "clinical_summary": "overall_health_assessment",
  "recommendations": ["recommendation_1", "recommendation_2"]
}"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please analyze this lab report image thoroughly and extract all medical data in the specified JSON format. Be precise with values and include clinical interpretations."
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
    
    print("🚀 Sending to OpenAI GPT-4 Vision...")
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
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
            analysis_file = "openai_lab_analysis.json"
            with open(analysis_file, 'w') as f:
                json.dump({
                    "image_analyzed": str(image_path),
                    "model_used": "gpt-4o",
                    "analysis_content": ai_content,
                    "usage_stats": usage,
                    "raw_response": result
                }, f, indent=2)
            
            print(f"💾 Analysis saved to: {analysis_file}")
            
            # Show usage stats
            print(f"\n📊 API Usage:")
            print(f"   Total Tokens: {usage.get('total_tokens', 'N/A')}")
            print(f"   Cost Estimate: ~${usage.get('total_tokens', 0) * 0.00001:.4f}")
            
            return ai_content
            
        else:
            print(f"❌ OpenAI API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    result = analyze_with_openai()
    if result:
        print("\n🎉 Lab report successfully analyzed!")
    else:
        print("\n😞 Analysis failed")