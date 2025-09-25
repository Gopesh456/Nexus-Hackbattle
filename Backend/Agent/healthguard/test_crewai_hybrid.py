#!/usr/bin/env python3
"""
Test the complete CrewAI system with hybrid Groq integration
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

def test_crewai_hybrid():
    """Test the CrewAI system with hybrid processing"""
    
    print("🤖 Testing CrewAI Hybrid Lab Analysis System")
    print("=" * 45)
    
    # Check API key
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found")
        return
    
    print(f"✅ Groq API Key configured")
    
    try:
        # Import the hybrid tool directly
        from src.healthguard.tools.hybrid_groq_processor import hybrid_groq_lab_processor
        
        print("✅ Hybrid Groq processor imported successfully")
        print("🔄 Testing hybrid processing...")
        
        # Test the tool
        result = hybrid_groq_lab_processor._run()
        
        if result.get("status") == "completed":
            print("✅ CrewAI Hybrid Processing SUCCESS!")
            print("\n📊 Processing Summary:")
            summary = result.get("processing_summary", {})
            print(f"   Total Images: {summary.get('total_images', 'N/A')}")
            print(f"   Successful: {summary.get('successful_processing', 'N/A')}")
            print(f"   Processing Time: {summary.get('total_processing_time', 'N/A'):.2f}s")
            print(f"   Method: {summary.get('processing_method', 'N/A')}")
            print(f"   Model: {summary.get('groq_model', 'N/A')}")
            
            # Show first result preview
            if result.get("results"):
                first_result = result["results"][0]
                if "error" not in first_result:
                    print(f"\n🎯 Analysis Preview:")
                    analysis = first_result.get("groq_analysis", "")[:200]
                    print(f"   {analysis}...")
                    
                    tokens = first_result.get("groq_processing_details", {}).get("tokens_consumed", 0)
                    print(f"   Tokens Used: {tokens}")
        else:
            print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ CrewAI test failed: {e}")
        
        # Fallback: test standalone hybrid processor
        print("\n🔄 Testing standalone hybrid processor...")
        try:
            from hybrid_lab_processor import process_lab_report_hybrid
            result = process_lab_report_hybrid()
            if result:
                print("✅ Standalone hybrid processor works!")
            else:
                print("❌ Standalone test also failed")
        except Exception as e2:
            print(f"❌ Standalone test failed: {e2}")

if __name__ == "__main__":
    test_crewai_hybrid()