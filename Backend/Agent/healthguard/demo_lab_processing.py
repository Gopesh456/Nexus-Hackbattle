#!/usr/bin/env python
"""
Comprehensive Demo: Lab Report Image Processing System

This script demonstrates how to:
1. Process lab report images and extract data
2. Integrate with the database system
3. Use with CrewAI health agents
4. Handle various image formats and quality levels

Run this after installing dependencies and setting up Django.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add project paths
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / "src" / "healthguard" / "tools"))
sys.path.append(str(current_dir / ".." / ".." / "nexus"))

print("🔬 Lab Report Image Processing System Demo")
print("=" * 60)

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking Dependencies...")
    
    dependencies = {
        'opencv-python': 'cv2',
        'pytesseract': 'pytesseract',
        'Pillow': 'PIL',
        'numpy': 'numpy'
    }
    
    missing_deps = []
    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing_deps.append(package)
    
    if missing_deps:
        print(f"\n🚨 Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install -r lab_processing_requirements.txt")
        return False
    
    # Check Tesseract OCR
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("  ✅ Tesseract OCR Engine")
    except Exception:
        print("  ❌ Tesseract OCR Engine - Install from https://github.com/tesseract-ocr/tesseract")
        print("     Windows: Download installer")
        print("     macOS: brew install tesseract")
        print("     Linux: sudo apt-get install tesseract-ocr")
        return False
    
    print("✅ All dependencies are available!\n")
    return True

def demo_image_processor():
    """Demonstrate the image processing capabilities."""
    print("📸 Image Processing Demo...")
    
    try:
        from lab_report_processor import LabReportImageProcessor
        
        processor = LabReportImageProcessor()
        print("✅ Lab Report Image Processor initialized")
        
        # Show supported parameters
        params = list(processor.common_lab_parameters.keys())[:10]
        print(f"🔬 Supports {len(processor.common_lab_parameters)} lab parameters including:")
        print(f"   {', '.join(params)}...")
        
        # Demonstrate text parsing (without actual image)
        sample_text = """
        COMPREHENSIVE METABOLIC PANEL
        Patient: John Doe        Age: 45
        Date: 2025-09-25
        
        Glucose         95    mg/dL    (70-100)
        Cholesterol    180    mg/dL    (<200)
        HDL             45    mg/dL    (>40)
        LDL            120    mg/dL    (<100)
        Creatinine     1.0    mg/dL    (0.6-1.2)
        """
        
        print("\n📝 Analyzing sample lab text...")
        parsed_data = processor.parse_lab_parameters(sample_text)
        analysis = processor.analyze_results(parsed_data)
        
        print(f"✅ Extracted {len(parsed_data['lab_results'])} parameters:")
        for param, data in parsed_data['lab_results'].items():
            print(f"   • {param.replace('_', ' ').title()}: {data['value']} {data.get('unit', '')}")
        
        print(f"\n💡 Analysis: {analysis['interpretation_summary']}")
        
        if analysis['interpretation_abnormalities']:
            print("🚨 Abnormalities found:")
            for abnormal in analysis['interpretation_abnormalities']:
                print(f"   • {abnormal}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import processor: {e}")
        print("Make sure dependencies are installed!")
        return False
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return False

def demo_integrated_tool():
    """Demonstrate the integrated tool capabilities."""
    print("🔧 Integrated Tool Demo...")
    
    try:
        from integrated_lab_processor import IntegratedLabReportTool, LabReportProcessorTool
        
        # Initialize tool
        tool = IntegratedLabReportTool(user_id=1, django_setup=False)  # Skip Django for demo
        print("✅ Integrated Lab Report Tool initialized")
        
        # Check status
        status = tool.get_processing_status()
        print(f"📊 Processing Capabilities:")
        print(f"   Image Processing: {'✅' if status['image_processing_available'] else '❌'}")
        print(f"   Database Integration: {'✅' if status['database_integration_available'] else '❌'}")
        print(f"   Features: {', '.join(status['features'])}")
        
        # Demo text processing
        sample_text = """
        LIPID PROFILE
        Total Cholesterol: 220 mg/dL (Normal: <200)
        HDL Cholesterol: 38 mg/dL (Normal: >40)
        LDL Cholesterol: 155 mg/dL (Normal: <100)
        Triglycerides: 180 mg/dL (Normal: <150)
        """
        
        print("\n🧪 Processing sample lab text...")
        result = tool.process_lab_text(sample_text, save_to_db=False)
        
        if result['success']:
            print(f"✅ Processing successful!")
            print(f"   Test: {result['lab_test_name']}")
            print(f"   Parameters: {result['parameters_extracted']}")
            print(f"   Confidence: {result['confidence_score']:.2f}")
            print(f"   Severity: {result['severity_level']}")
            
            if result['interpretation_abnormalities']:
                print("   🚨 Abnormalities:")
                for abnormal in result['interpretation_abnormalities']:
                    print(f"     • {abnormal}")
        else:
            print(f"❌ Processing failed: {result['error']}")
        
        # Demo CrewAI tool wrapper
        print("\n🤖 CrewAI Tool Wrapper Demo...")
        crew_tool = LabReportProcessorTool(user_id=1)
        print("✅ CrewAI compatible tool ready")
        print("   Usage: crew_tool.process_lab_image('path/to/image.jpg')")
        print("   Usage: crew_tool.get_lab_history('Blood Chemistry')")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import integrated tool: {e}")
        return False
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return False

def demo_api_usage():
    """Demonstrate API usage examples."""
    print("🌐 API Usage Examples...")
    
    print("📤 Image Upload API:")
    print("""
    # Upload lab report image
    curl -X POST http://localhost:8000/healthapp/api/lab-image-upload/ \\
         -F "lab_report_image=@lab_report.jpg" \\
         -F "user_id=1"
    
    # Or with base64 encoding
    curl -X POST http://localhost:8000/healthapp/api/lab-image-upload/ \\
         -H "Content-Type: application/json" \\
         -d '{"image_base64": "base64_encoded_image_data", "user_id": 1}'
    """)
    
    print("📝 Text Analysis API:")
    print("""
    curl -X POST http://localhost:8000/healthapp/api/lab-text-analyze/ \\
         -H "Content-Type: application/json" \\
         -d '{"lab_text": "Glucose: 95 mg/dL...", "user_id": 1}'
    """)
    
    print("📊 Check Processing Status:")
    print("""
    curl -X GET http://localhost:8000/healthapp/api/lab-status/
    """)
    
    print("🔄 Batch Processing:")
    print("""
    curl -X POST http://localhost:8000/healthapp/api/lab-batch-process/ \\
         -F "lab_report_1=@report1.jpg" \\
         -F "lab_report_2=@report2.jpg" \\
         -F "user_id=1"
    """)

def demo_workflow_examples():
    """Show complete workflow examples."""
    print("🔄 Complete Workflow Examples...")
    
    print("1️⃣ Single Image Processing Workflow:")
    print("""
    from integrated_lab_processor import IntegratedLabReportTool
    
    # Initialize tool
    processor = IntegratedLabReportTool(user_id=1)
    
    # Process lab report image
    result = processor.process_lab_image_from_path('lab_report.jpg')
    
    if result['success']:
        print(f"Extracted {result['parameters_extracted']} parameters")
        print(f"Summary: {result['interpretation_summary']}")
        
        # Compare with previous results
        comparison = processor.compare_with_previous_results(result)
        if comparison['success']:
            print(f"Trends: {comparison['comparison']['trends']}")
    """)
    
    print("2️⃣ CrewAI Agent Integration:")
    print("""
    from integrated_lab_processor import LabReportProcessorTool
    
    class LabAgent:
        def __init__(self):
            self.lab_tool = LabReportProcessorTool(user_id=1)
        
        def process_patient_lab(self, image_path):
            # Process the lab report
            result = self.lab_tool.process_lab_image(image_path)
            
            # Get historical data for context
            history = self.lab_tool.get_lab_history()
            
            return f"Current Results: {result}\\n\\nHistory: {history}"
    """)
    
    print("3️⃣ Batch Processing Workflow:")
    print("""
    import os
    from integrated_lab_processor import IntegratedLabReportTool
    
    processor = IntegratedLabReportTool(user_id=1)
    
    # Process all images in a folder
    lab_folder = 'path/to/lab_reports/'
    results = []
    
    for filename in os.listdir(lab_folder):
        if filename.lower().endswith(('.jpg', '.png', '.tiff')):
            image_path = os.path.join(lab_folder, filename)
            result = processor.process_lab_image_from_path(image_path)
            results.append(result)
    
    # Analyze batch results
    successful = sum(1 for r in results if r['success'])
    print(f"Processed {successful}/{len(results)} images successfully")
    """)

def show_setup_instructions():
    """Display setup instructions."""
    print("🚀 Setup Instructions...")
    
    print("1️⃣ Install Dependencies:")
    print("   pip install -r lab_processing_requirements.txt")
    
    print("\n2️⃣ Install Tesseract OCR:")
    print("   Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    print("   macOS: brew install tesseract")
    print("   Linux: sudo apt-get install tesseract-ocr")
    
    print("\n3️⃣ Setup Django Database:")
    print("   cd Backend/nexus")
    print("   python manage.py makemigrations healthapp")
    print("   python manage.py migrate")
    
    print("\n4️⃣ Start Django Server:")
    print("   python manage.py runserver")
    
    print("\n5️⃣ Test API Endpoints:")
    print("   GET http://localhost:8000/healthapp/api/lab-status/")
    print("   POST http://localhost:8000/healthapp/api/lab-image-upload/")

def main():
    """Run the complete demo."""
    try:
        # Check dependencies
        if not check_dependencies():
            print("\n🔧 Please install missing dependencies first!")
            show_setup_instructions()
            return
        
        # Run demos
        print("🎯 Running Demonstrations...\n")
        
        success_count = 0
        
        if demo_image_processor():
            success_count += 1
        print()
        
        if demo_integrated_tool():
            success_count += 1
        print()
        
        demo_api_usage()
        print()
        
        demo_workflow_examples()
        print()
        
        # Summary
        print("📊 Demo Summary")
        print("=" * 30)
        print(f"✅ Successful demos: {success_count}/2")
        
        if success_count == 2:
            print("🎉 All systems operational!")
            print("\n💡 Next Steps:")
            print("1. Setup Django database migrations")
            print("2. Start Django server")
            print("3. Test with real lab report images")
            print("4. Integrate with your CrewAI health agents")
        else:
            print("⚠️  Some issues detected. Please check the errors above.")
            print("\n🔧 Troubleshooting:")
            print("1. Ensure all dependencies are installed")
            print("2. Check Tesseract OCR installation")
            print("3. Verify Python environment setup")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("\nPlease check the setup instructions and try again.")

if __name__ == "__main__":
    main()