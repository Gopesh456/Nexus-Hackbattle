#!/usr/bin/env python3
"""
Test script for Groq Vision Lab Report Processing

This script demonstrates the base64 conversion and Groq API integration
for analyzing lab report images.
"""

import os
import sys
import base64
import json
from pathlib import Path
from datetime import datetime

def convert_image_to_base64(image_path):
    """Convert image to base64 for Groq API"""
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            return base64_encoded, len(image_data)
    except Exception as e:
        print(f"Error converting image: {e}")
        return None, 0

def test_groq_integration():
    """Test the Groq vision integration"""
    
    print("🏥 Testing Groq Vision Lab Report Integration")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("\n⚠️  GROQ_API_KEY not found in environment variables")
        print("Please set your Groq API key:")
        print("$env:GROQ_API_KEY='your-api-key-here'  # PowerShell")
        print("\nGet your API key from: https://console.groq.com/keys")
        return
    
    print(f"✅ Groq API Key configured (ends with: ...{api_key[-4:]})")
    
    # Find lab report images
    images_folder = Path("Backend/Agent/images")
    if not images_folder.exists():
        print(f"❌ Images folder not found: {images_folder}")
        return
    
    # Get available images
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_files.extend(list(images_folder.glob(ext)))
    
    if not image_files:
        print("❌ No lab report images found")
        return
    
    print(f"📸 Found {len(image_files)} image(s):")
    for img in image_files:
        print(f"   • {img.name}")
    
    # Process first image
    test_image = image_files[0]
    print(f"\n🔄 Processing: {test_image.name}")
    
    # Convert to base64
    base64_data, file_size = convert_image_to_base64(test_image)
    if not base64_data:
        return
    
    print(f"✅ Converted to base64 (size: {file_size:,} bytes)")
    print(f"   Base64 length: {len(base64_data):,} characters")
    
    # Test Groq API call (mock structure)
    groq_request = {
        "model": "llama-3.2-90b-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert medical AI assistant. Analyze the lab report image and extract all medical data."
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": "Please analyze this lab report image and extract all medical parameters, values, and provide clinical insights."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_data}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4000,
        "temperature": 0.1
    }
    
    print(f"\n📋 Groq API Request Structure:")
    print(f"   Model: {groq_request['model']}")
    print(f"   Max Tokens: {groq_request['max_tokens']}")
    print(f"   Temperature: {groq_request['temperature']}")
    print(f"   Image Data: Ready for transmission")
    
    # Save request structure for debugging
    debug_file = f"groq_request_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Create a version without the large base64 data for debugging
    debug_request = groq_request.copy()
    debug_request['messages'][1]['content'][1]['image_url']['url'] = f"data:image/jpeg;base64,[{len(base64_data)} characters]"
    
    with open(debug_file, 'w') as f:
        json.dump(debug_request, f, indent=2)
    
    print(f"💾 Request structure saved to: {debug_file}")
    
    # Show expected response structure
    print(f"\n📊 Expected Groq Response Structure:")
    expected_response = {
        "processing_info": {
            "image_source": str(test_image),
            "groq_model": "llama-3.2-90b-vision-preview",
            "base64_size": file_size,
            "processing_time": "TBD",
            "api_response_tokens": "TBD"
        },
        "lab_test_name": "Extracted by Groq AI",
        "patient_name": "Extracted by Groq AI", 
        "lab_results": {
            "parameter_1": {
                "value": "AI_extracted_value",
                "unit": "AI_extracted_unit",
                "status": "normal/abnormal/critical"
            }
        },
        "groq_ai_insights": {
            "clinical_summary": "AI-generated summary",
            "risk_assessment": "AI risk analysis",
            "follow_up_recommendations": ["AI recommendations"]
        }
    }
    
    for key, value in list(expected_response.items())[:5]:
        if isinstance(value, dict):
            print(f"   {key}: {{...}}")
        else:
            print(f"   {key}: {value}")
    
    print("\n✅ Groq Integration Test Completed!")
    print("\nNext Steps:")
    print("1. Set GROQ_API_KEY environment variable")
    print("2. Run: python -m src.healthguard.tools.groq_vision_processor")
    print("3. Or use the CrewAI labs_task which will automatically process images")

if __name__ == "__main__":
    test_groq_integration()