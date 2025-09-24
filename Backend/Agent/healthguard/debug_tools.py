#!/usr/bin/env python3
"""
Standalone debugging script for HealthGuard custom tools.
This script allows you to test each tool individually without running the full CrewAI setup.
"""

import os
import sys
import json
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import the tools directly
try:
    from healthguard.tools.custom_tool import (
        BrowserTool, 
        WebSearchTool, 
        JSONStorageTool, 
        JSONResponseTool, 
        JSONProcessorTool
    )
    print("✅ Successfully imported all tools")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the healthguard project root directory")
    sys.exit(1)

def test_json_storage_tool():
    """Test the JSON Storage Tool"""
    print("\n" + "="*50)
    print("🧪 TESTING JSON STORAGE TOOL")
    print("="*50)
    
    tool = JSONStorageTool()
    
    # Test cases
    test_cases = [
        {
            "prompt": "I have been experiencing headaches for 3 days",
            "filename": "health_test",
            "category": "health"
        },
        {
            "prompt": "Need to book appointment with cardiologist",
            "filename": "appointment_test", 
            "category": "appointment"
        },
        {
            "prompt": "Can I take aspirin with my current medication?",
            "filename": "medication_test",
            "category": "medication"
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['category'].title()}")
        print(f"Prompt: {test_case['prompt']}")
        
        try:
            result = tool._run(**test_case)
            print(f"✅ Result: {result}")
            results.append({"success": True, "result": result, "test_case": test_case})
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({"success": False, "error": str(e), "test_case": test_case})
    
    return results

def test_json_response_tool():
    """Test the JSON Response Tool"""
    print("\n" + "="*50)
    print("🧪 TESTING JSON RESPONSE TOOL")
    print("="*50)
    
    tool = JSONResponseTool()
    
    # Test cases
    test_cases = [
        {
            "response_data": '{"diagnosis": "preliminary assessment needed", "urgency": "medium"}',
            "prompt_id": "health_test_20240924_000001",
            "response_type": "health",
            "filename": "health_response"
        },
        {
            "response_data": "Simple text response for testing",
            "prompt_id": "general_test_20240924_000002",
            "response_type": "general",
            "filename": "general_response"
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['response_type'].title()} Response")
        print(f"Response Data: {test_case['response_data'][:50]}...")
        
        try:
            result = tool._run(**test_case)
            print(f"✅ Result: {result}")
            results.append({"success": True, "result": result, "test_case": test_case})
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({"success": False, "error": str(e), "test_case": test_case})
    
    return results

def test_json_processor_tool():
    """Test the JSON Processor Tool"""
    print("\n" + "="*50)
    print("🧪 TESTING JSON PROCESSOR TOOL")
    print("="*50)
    
    tool = JSONProcessorTool()
    
    # First, create some test files to process
    data_dir = Path("data")
    if not data_dir.exists():
        print("No data directory found. Creating test files first...")
        test_json_storage_tool()
    
    # Find JSON prompt files to test
    if data_dir.exists():
        prompt_files = list(data_dir.glob("*_prompt.json"))
        
        if not prompt_files:
            print("No prompt files found. Creating a test file...")
            # Create a simple test file
            test_data = {
                "id": "debug_test_20240924_000000",
                "timestamp": "2024-09-24T12:00:00",
                "category": "health",
                "prompt": "I have a headache and feel dizzy",
                "status": "stored",
                "processed": False
            }
            
            test_file = data_dir / "debug_test_prompt.json"
            with open(test_file, 'w') as f:
                json.dump(test_data, f, indent=2)
            
            prompt_files = [test_file]
        
        results = []
        for i, file_path in enumerate(prompt_files[:3], 1):  # Test only first 3 files
            print(f"\nTest Case {i}: Processing {file_path.name}")
            
            try:
                result = tool._run(prompt_file=str(file_path))
                print(f"✅ Result: {result}")
                results.append({"success": True, "result": result, "file": str(file_path)})
            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({"success": False, "error": str(e), "file": str(file_path)})
        
        return results
    else:
        print("❌ Could not create or find data directory")
        return []

def test_browser_tool():
    """Test the Browser Tool (if API key available)"""
    print("\n" + "="*50)
    print("🧪 TESTING BROWSER TOOL")
    print("="*50)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OPENAI_API_KEY not found. Browser tool will run in test mode.")
        print("   Set OPENAI_API_KEY environment variable for full testing.")
    
    tool = BrowserTool()
    
    # Simple test case
    test_task = "Search for 'healthcare' and get basic information"
    
    print(f"\nTest Task: {test_task}")
    
    try:
        result = tool._run(task=test_task)
        print(f"✅ Result: {result}")
        return {"success": True, "result": result}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"success": False, "error": str(e)}

def test_web_search_tool():
    """Test the Web Search Tool (if API key available)"""
    print("\n" + "="*50)
    print("🧪 TESTING WEB SEARCH TOOL")
    print("="*50)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OPENAI_API_KEY not found. Web search tool will run in test mode.")
        print("   Set OPENAI_API_KEY environment variable for full testing.")
    
    tool = WebSearchTool()
    
    # Simple test case
    test_query = "hospitals near me"
    
    print(f"\nTest Query: {test_query}")
    
    try:
        result = tool._run(query=test_query)
        print(f"✅ Result: {result}")
        return {"success": True, "result": result}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"success": False, "error": str(e)}

def show_data_files():
    """Show generated data files"""
    print("\n" + "="*50)
    print("📁 GENERATED DATA FILES")
    print("="*50)
    
    data_dir = Path("data")
    if data_dir.exists():
        files = list(data_dir.glob("*.json"))
        
        if files:
            print(f"\nFound {len(files)} JSON files in data/ directory:")
            for file in sorted(files):
                file_size = file.stat().st_size
                print(f"  📄 {file.name} ({file_size} bytes)")
                
                # Show brief content
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        if 'category' in data:
                            print(f"      Category: {data.get('category', 'N/A')}")
                        if 'response_type' in data:
                            print(f"      Response Type: {data.get('response_type', 'N/A')}")
                except Exception as e:
                    print(f"      Error reading file: {e}")
        else:
            print("No JSON files found in data/ directory.")
    else:
        print("No data/ directory found.")

def run_all_tests():
    """Run all tool tests"""
    print("🚀 Starting HealthGuard Custom Tools Debug Session")
    print("="*60)
    
    # Check environment
    print("\n📋 ENVIRONMENT CHECK")
    print("-"*30)
    print(f"Working Directory: {os.getcwd()}")
    print(f"Python Path: {sys.path[0]}")
    print(f"OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
    
    # Run tests
    tests = [
        ("JSON Storage Tool", test_json_storage_tool),
        ("JSON Response Tool", test_json_response_tool), 
        ("JSON Processor Tool", test_json_processor_tool),
        ("Browser Tool", test_browser_tool),
        ("Web Search Tool", test_web_search_tool)
    ]
    
    all_results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            all_results[test_name] = result
        except Exception as e:
            print(f"❌ Fatal error in {test_name}: {e}")
            all_results[test_name] = {"fatal_error": str(e)}
    
    # Show data files
    show_data_files()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, result in all_results.items():
        if isinstance(result, dict) and "fatal_error" in result:
            print(f"❌ {test_name}: Fatal Error")
        elif isinstance(result, list):
            success_count = sum(1 for r in result if r.get("success", False))
            total_count = len(result)
            print(f"{'✅' if success_count == total_count else '⚠️ '} {test_name}: {success_count}/{total_count} passed")
        elif isinstance(result, dict):
            print(f"{'✅' if result.get('success', False) else '❌'} {test_name}: {'Passed' if result.get('success', False) else 'Failed'}")
        else:
            print(f"❓ {test_name}: Unknown result format")

def interactive_mode():
    """Interactive mode for testing individual tools"""
    print("\n🔧 INTERACTIVE TESTING MODE")
    print("="*40)
    
    tools_map = {
        "1": ("JSON Storage", test_json_storage_tool),
        "2": ("JSON Response", test_json_response_tool),
        "3": ("JSON Processor", test_json_processor_tool),
        "4": ("Browser Tool", test_browser_tool),
        "5": ("Web Search", test_web_search_tool),
        "6": ("Show Data Files", show_data_files),
        "7": ("Run All Tests", run_all_tests)
    }
    
    while True:
        print("\nSelect a tool to test:")
        for key, (name, _) in tools_map.items():
            print(f"  {key}. {name}")
        print("  0. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice in tools_map:
            name, func = tools_map[choice]
            print(f"\n🏃 Running {name}...")
            try:
                func()
            except Exception as e:
                print(f"❌ Error running {name}: {e}")
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        run_all_tests()
        print(f"\n💡 Tip: Run with --interactive flag for interactive mode")
        print(f"   python debug_tools.py --interactive")