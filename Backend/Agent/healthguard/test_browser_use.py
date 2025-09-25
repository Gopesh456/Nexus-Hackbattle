#!/usr/bin/env python3
"""Test script to verify browser-use integration with CrewAI"""

import os
from healthguard.tools.custom_tool import browser_tool, web_search_tool

def test_browser_tool():
    """Test the browser automation tool"""
    print("Testing Browser Tool...")
    try:
        # Test browser tool with a simple task
        result = browser_tool._run("Search Google for 'healthcare near me' and get the top result")
        print(f"Browser Tool Result: {result}")
        return True
    except Exception as e:
        print(f"Browser Tool Error: {e}")
        return False

def test_web_search_tool():
    """Test the web search tool"""
    print("Testing Web Search Tool...")
    try:
        # Test web search tool
        result = web_search_tool._run("hospitals in New York")
        print(f"Web Search Tool Result: {result}")
        return True
    except Exception as e:
        print(f"Web Search Tool Error: {e}")
        return False

def test_crew_integration():
    """Test CrewAI integration with browser tools"""
    print("Testing CrewAI Integration...")
    try:
        from healthguard.crew import Healthguard
        
        # Create Healthguard crew
        crew = Healthguard()
        print("CrewAI integration successful!")
        return True
    except Exception as e:
        print(f"CrewAI Integration Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Browser Use Integration Test")
    print("=" * 50)
    
    # Set environment variables if needed
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY not set. Some features may not work.")
    
    # Run tests
    tests = [
        ("CrewAI Integration", test_crew_integration),
        ("Browser Tool", test_browser_tool),
        ("Web Search Tool", test_web_search_tool),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        results[test_name] = test_func()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    if all(results.values()):
        print("\n🎉 All tests passed! Browser-use integration is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")