#!/usr/bin/env python3
"""
Demo script showing base64 conversion for lab report images
(Works without Groq API key for demonstration)
"""

import base64
import json
from pathlib import Path
from datetime import datetime

def demo_base64_conversion():
    """Demo the base64 conversion process"""
    
    print("🏥 Lab Report Base64 Conversion Demo")
    print("=" * 40)
    
    # Find lab report images
    images_folder = Path("../images")
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
    
    try:
        # Convert to base64
        with open(test_image, 'rb') as image_file:
            image_data = image_file.read()
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
        
        file_size = len(image_data)
        base64_size = len(base64_encoded)
        
        print(f"✅ Successfully converted to base64!")
        print(f"   Original file size: {file_size:,} bytes")
        print(f"   Base64 size: {base64_size:,} characters")
        print(f"   Size increase: {(base64_size/file_size)*100:.1f}%")
        
        # Show first and last 50 characters of base64
        print(f"\n📋 Base64 Preview:")
        print(f"   Start: {base64_encoded[:50]}...")
        print(f"   End: ...{base64_encoded[-50:]}")
        
        # Create the Groq API payload structure
        groq_payload = {
            "model": "llama-3.2-90b-vision-preview",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert medical AI assistant specializing in lab report analysis. Extract ALL visible medical data with high accuracy."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Please analyze this lab report image ({test_image.name}) and extract all medical data in JSON format."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_encoded}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.1
        }
        
        print(f"\n🚀 Ready for Groq API!")
        print(f"   Model: {groq_payload['model']}")
        print(f"   Max Tokens: {groq_payload['max_tokens']}")
        print(f"   Image Data: ✅ Encoded and ready")
        
        # Save a debug version (without the large base64 data)
        debug_payload = groq_payload.copy()
        debug_payload['messages'][1]['content'][1]['image_url']['url'] = f"data:image/jpeg;base64,[BASE64_DATA_{base64_size}_CHARS]"
        
        debug_file = f"groq_payload_structure.json"
        with open(debug_file, 'w') as f:
            json.dump(debug_payload, f, indent=2)
        
        print(f"💾 Payload structure saved to: {debug_file}")
        
        # Show what happens next
        print(f"\n📊 What happens when sent to Groq:")
        print(f"   1. Image is processed by Groq's vision AI")
        print(f"   2. AI extracts patient info, lab values, ranges")
        print(f"   3. AI provides clinical insights and recommendations")
        print(f"   4. Response formatted as structured JSON")
        
        print(f"\n✅ Base64 conversion completed successfully!")
        print(f"   Your lab report is ready for AI analysis!")
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")

if __name__ == "__main__":
    demo_base64_conversion()