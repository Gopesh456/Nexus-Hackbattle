#!/usr/bin/env python3
"""
Direct debugging script for HealthGuard custom tools.
This script imports and tests tools directly without module imports.
"""

import os
import sys
import json
import datetime
from pathlib import Path

print("🚀 HealthGuard Custom Tools Direct Debug")
print("="*50)

# Set up environment
current_dir = Path(__file__).parent
tools_file = current_dir / "src" / "healthguard" / "tools" / "custom_tool.py"

print(f"Current Directory: {current_dir}")
print(f"Looking for tools at: {tools_file}")
print(f"Tools file exists: {tools_file.exists()}")

if not tools_file.exists():
    print("❌ custom_tool.py not found!")
    sys.exit(1)

# Add src to path and try to import
sys.path.insert(0, str(current_dir / "src"))

try:
    # Import the tools module
    exec(open(tools_file).read())
    
    print("✅ Successfully loaded custom_tool.py")
    
    # Test JSON Storage Tool
    print("\n" + "="*40)
    print("🧪 TESTING JSON STORAGE TOOL")
    print("="*40)
    
    storage_tool = JSONStorageTool()
    
    test_prompt = "I have been experiencing headaches and dizziness for 3 days"
    print(f"Test prompt: {test_prompt}")
    
    try:
        result = storage_tool._run(
            prompt=test_prompt,
            filename="debug_health",
            category="health"
        )
        print(f"✅ JSON Storage Result: {result}")
    except Exception as e:
        print(f"❌ JSON Storage Error: {e}")
    
    # Test JSON Response Tool
    print("\n" + "="*40)
    print("🧪 TESTING JSON RESPONSE TOOL")
    print("="*40)
    
    response_tool = JSONResponseTool()
    
    test_response = {
        "analysis": "Preliminary health assessment",
        "urgency": "medium",
        "recommendations": ["Monitor symptoms", "Consult doctor if symptoms persist"]
    }
    
    try:
        result = response_tool._run(
            response_data=json.dumps(test_response),
            prompt_id="debug_health_20240924_120000",
            response_type="health",
            filename="debug_response"
        )
        print(f"✅ JSON Response Result: {result}")
    except Exception as e:
        print(f"❌ JSON Response Error: {e}")
    
    # Test JSON Processor Tool
    print("\n" + "="*40)
    print("🧪 TESTING JSON PROCESSOR TOOL")
    print("="*40)
    
    processor_tool = JSONProcessorTool()
    
    # Check for existing prompt files
    data_dir = Path("data")
    if data_dir.exists():
        prompt_files = list(data_dir.glob("*_prompt.json"))
        if prompt_files:
            test_file = prompt_files[0]
            print(f"Testing with file: {test_file}")
            
            try:
                result = processor_tool._run(prompt_file=str(test_file))
                print(f"✅ JSON Processor Result: {result}")
            except Exception as e:
                print(f"❌ JSON Processor Error: {e}")
        else:
            print("⚠️ No prompt files found to process")
    else:
        print("⚠️ No data directory found")
    
    # Test Browser Tool (basic)
    print("\n" + "="*40)
    print("🧪 TESTING BROWSER TOOL (BASIC)")
    print("="*40)
    
    browser_tool = BrowserTool()
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"OpenAI API Key: {'✅ Set' if api_key else '❌ Not set'}")
    
    if api_key:
        print("Running browser tool with API key...")
        try:
            result = browser_tool._run(task="Get the title of google.com")
            print(f"✅ Browser Tool Result: {result[:200]}...")
        except Exception as e:
            print(f"❌ Browser Tool Error: {e}")
    else:
        print("⚠️ Skipping browser tool test (no API key)")
    
    # Show generated files
    print("\n" + "="*40)
    print("📁 GENERATED FILES")
    print("="*40)
    
    if data_dir.exists():
        files = list(data_dir.glob("*.json"))
        print(f"Found {len(files)} JSON files:")
        for file in sorted(files):
            size = file.stat().st_size
            print(f"  📄 {file.name} ({size} bytes)")
    else:
        print("No data directory found")
    
    print("\n✅ Debug session completed!")

except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()

print("\n💡 Tips:")
print("  - Set OPENAI_API_KEY for browser tool testing")
print("  - Check data/ directory for generated JSON files")
print("  - Run from the healthguard project root directory")