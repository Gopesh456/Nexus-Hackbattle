#!/usr/bin/env python3
"""
Example script demonstrating Groq Vision Lab Report Processing

This script shows how to use the Groq-powered lab report processor to:
1. Scan images folder for lab reports
2. Convert images to base64 for API transmission
3. Send to Groq's vision models for AI analysis
4. Extract comprehensive medical data and insights

Requirements:
- GROQ_API_KEY environment variable set
- Images stored in the images folder
- All dependencies installed from requirements.txt

Usage:
    python groq_lab_demo.py
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Set up environment
os.environ.setdefault('GROQ_API_KEY', 'your-groq-api-key-here')

# Import the Groq vision processor
from src.healthguard.tools.groq_vision_processor import groq_vision_processor

def main():
    """Demonstrate Groq vision processing for lab reports"""
    
    print("🏥 Healthguard Groq Vision Lab Report Processor Demo")
    print("=" * 60)
    
    try:
        # Check if GROQ_API_KEY is set
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key or api_key == 'your-groq-api-key-here':
            print("❌ ERROR: Please set your GROQ_API_KEY environment variable")
            print("   Get your API key from: https://console.groq.com/keys")
            return
        
        print(f"✅ Groq API Key configured")
        
        # Initialize processor
        print("🔄 Initializing Groq Vision Processor...")
        
        # Process all lab report images in the images folder
        print("📸 Processing lab report images...")
        result = groq_vision_processor._run()
        
        # Display results
        print("\n📊 Processing Results:")
        print("-" * 40)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return
        
        # Summary
        summary = result.get('processing_summary', {})
        print(f"Total Images Processed: {summary.get('total_images', 0)}")
        print(f"Successful: {summary.get('successful_processing', 0)}")
        print(f"Failed: {summary.get('failed_processing', 0)}")
        print(f"Processing Time: {summary.get('total_processing_time', 0):.2f} seconds")
        
        # Individual results
        results = result.get('results', [])
        for i, lab_result in enumerate(results, 1):
            print(f"\n📋 Lab Report #{i}:")
            
            if "error" in lab_result:
                print(f"   ❌ Error: {lab_result['error']}")
                continue
            
            # Basic info
            processing_info = lab_result.get('processing_info', {})
            print(f"   🖼️  Image: {Path(processing_info.get('image_source', 'Unknown')).name}")
            print(f"   🤖 Model: {processing_info.get('groq_model', 'Unknown')}")
            print(f"   🏥 Lab Test: {lab_result.get('lab_test_name', 'Unknown')}")
            print(f"   👤 Patient: {lab_result.get('patient_name', 'Unknown')}")
            print(f"   📅 Date: {lab_result.get('report_date', 'Unknown')}")
            
            # Lab results
            lab_results = lab_result.get('lab_results', {})
            if lab_results:
                print(f"   🧪 Parameters Found: {len(lab_results)}")
                for param, data in list(lab_results.items())[:3]:  # Show first 3
                    print(f"      • {param}: {data.get('value', 'N/A')} {data.get('unit', '')}")
                if len(lab_results) > 3:
                    print(f"      ... and {len(lab_results) - 3} more parameters")
            
            # AI Insights
            ai_insights = lab_result.get('groq_ai_insights', {})
            if ai_insights.get('clinical_summary'):
                print(f"   🧠 AI Summary: {ai_insights['clinical_summary'][:100]}...")
            
            # Quality metrics
            quality = lab_result.get('data_quality_metrics', {})
            confidence = quality.get('extraction_confidence', 0)
            print(f"   📈 Confidence: {confidence:.0%}")
        
        # Save detailed results to file
        output_file = f"groq_lab_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {output_file}")
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Make sure you have:")
        print("  1. Set GROQ_API_KEY environment variable")
        print("  2. Installed all requirements: pip install -r requirements.txt")
        print("  3. Lab report images in the images folder")

def check_setup():
    """Check if the setup is ready for the demo"""
    
    print("🔍 Checking setup...")
    
    # Check API key
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key or api_key == 'your-groq-api-key-here':
        print("❌ GROQ_API_KEY not set")
        return False
    else:
        print("✅ GROQ_API_KEY configured")
    
    # Check images folder
    images_folder = Path("images")
    if not images_folder.exists():
        print("❌ Images folder not found")
        return False
    
    # Check for image files
    image_files = list(images_folder.glob("*.jpg")) + list(images_folder.glob("*.jpeg")) + list(images_folder.glob("*.png"))
    if not image_files:
        print("❌ No lab report images found in images folder")
        return False
    else:
        print(f"✅ Found {len(image_files)} image files")
    
    # Check dependencies (basic check)
    try:
        import requests
        import PIL
        print("✅ Core dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Groq Vision Lab Report Demo")
    
    if check_setup():
        print("\n" + "="*60)
        main()
    else:
        print("\n❌ Setup incomplete. Please fix the issues above and try again.")