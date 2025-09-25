#!/usr/bin/env python3
"""
Quick test script to verify the lab analysis setup
"""

import os
import sys
from pathlib import Path

def test_setup():
    """Test if everything is set up correctly"""
    
    print("🧪 Lab Analysis Setup Test")
    print("=" * 30)
    
    # Test 1: Check Python version
    print(f"✅ Python version: {sys.version}")
    
    # Test 2: Check if images folder exists
    images_folder = Path("../images")
    if images_folder.exists():
        image_files = list(images_folder.glob("*.jpeg")) + list(images_folder.glob("*.jpg")) + list(images_folder.glob("*.png"))
        print(f"✅ Images folder found with {len(image_files)} image(s)")
        for img in image_files:
            print(f"   • {img.name}")
    else:
        print(f"❌ Images folder not found: {images_folder}")
        return False
    
    # Test 3: Check required modules
    required_modules = ['requests', 'base64', 'json', 'pathlib']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Module '{module}' available")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ Module '{module}' missing")
    
    if missing_modules:
        print(f"\n📦 Install missing modules with:")
        print(f"   pip install {' '.join(missing_modules)}")
        return False
    
    # Test 4: Check API key
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        print(f"✅ GROQ_API_KEY found (ends with: ...{api_key[-4:]})")
    else:
        print(f"⚠️  GROQ_API_KEY not found")
        print(f"   Run setup_api_key.py first or set it manually:")
        print(f"   $env:GROQ_API_KEY = 'your_api_key_here'")
        return False
    
    # Test 5: Check lab analysis script
    lab_script = Path("lab_analysis_llama_scout.py")
    if lab_script.exists():
        print(f"✅ Lab analysis script ready: {lab_script.name}")
    else:
        print(f"❌ Lab analysis script not found: {lab_script}")
        return False
    
    print(f"\n🎉 All tests passed! You can now run the lab analysis.")
    print(f"   Run: python lab_analysis_llama_scout.py")
    
    return True

if __name__ == "__main__":
    success = test_setup()
    if not success:
        print(f"\n❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)