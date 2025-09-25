"""
Lab Report API Test Script

This script demonstrates how to use the lab report endpoints to store and retrieve 
lab reports with base64 file data.
"""

import requests
import json
import base64
from datetime import datetime, date

# API Base URL
BASE_URL = "http://127.0.0.1:8000/api"

def create_sample_base64_file():
    """Create a sample base64 encoded file for testing"""
    # Create a simple text file content for testing
    sample_content = """
    MEDICAL LAB REPORT
    ==================
    
    Patient: John Doe
    Date: 2025-09-25
    Lab: City Medical Laboratory
    
    BLOOD TEST RESULTS:
    -------------------
    Hemoglobin: 14.5 g/dL (Normal: 12.0-16.0)
    WBC Count: 7,200/µL (Normal: 4,000-11,000)
    Glucose: 95 mg/dL (Normal: 70-100)
    Cholesterol: 180 mg/dL (Normal: <200)
    
    CONCLUSION:
    All values are within normal ranges.
    
    Dr. Smith, MD
    Licensed Medical Doctor
    """
    
    # Encode to base64
    encoded_content = base64.b64encode(sample_content.encode('utf-8')).decode('utf-8')
    return encoded_content

def test_lab_report_api():
    """Test the lab report endpoints"""
    
    # Replace with your actual JWT token
    JWT_TOKEN = "your_jwt_token_here"
    
    print("🧪 Testing Lab Report API")
    print("=" * 50)
    
    # Create sample base64 data
    base64_data = create_sample_base64_file()
    print(f"Created sample base64 data (length: {len(base64_data)} characters)")
    
    # Test data for storing a lab report
    lab_report_data = {
        "token": JWT_TOKEN,
        "report_name": "Blood Test Report - September 2025",
        "report_type": "blood_test",
        "lab_name": "City Medical Laboratory",
        "doctor_name": "Dr. Sarah Smith",
        "report_date": "2025-09-25",
        "file_data": base64_data,
        "file_name": "blood_test_report_sept_2025.txt",
        "file_type": "txt",
        "notes": "Routine annual blood work. All values normal."
    }
    
    # 1. Store lab report
    print("\n1. Storing lab report...")
    try:
        response = requests.post(f"{BASE_URL}/lab-reports/store/", json=lab_report_data)
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Success! Lab report stored:")
            print(f"   ID: {data['data']['id']}")
            print(f"   Report Name: {data['data']['report_name']}")
            print(f"   Type: {data['data']['report_type']}")
            print(f"   Lab: {data['data']['lab_name']}")
            print(f"   Doctor: {data['data']['doctor_name']}")
            print(f"   Date: {data['data']['report_date']}")
            print(f"   File: {data['data']['file_name']} ({data['data']['file_size_mb']} MB)")
            print(f"   Base64 stored: {data['file_stored']}")
            print(f"   Base64 length: {data['base64_length']}")
            
            stored_report_id = data['data']['id']
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure your Django server is running on http://127.0.0.1:8000")
        return
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return
    
    # 2. Get all lab reports (without file data)
    print("\n" + "=" * 50)
    print("\n2. Retrieving all lab reports (metadata only)...")
    try:
        response = requests.post(f"{BASE_URL}/lab-reports/get/", json={"token": JWT_TOKEN})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data['count']} lab report(s) for user: {data['user']}")
            
            if data['reports']:
                print("\nLab report summaries:")
                for i, report in enumerate(data['reports'], 1):
                    report_date = datetime.fromisoformat(report['report_date']).strftime('%B %d, %Y')
                    
                    print(f"\n   {i}. {report['report_name']}")
                    print(f"      📊 Type: {report['report_type'].replace('_', ' ').title()}")
                    print(f"      🏥 Lab: {report['lab_name']}")
                    print(f"      👨‍⚕️ Doctor: {report['doctor_name']}")
                    print(f"      📅 Date: {report_date}")
                    print(f"      📄 File: {report['file_name']} ({report['file_size_mb']} MB)")
                    print(f"      📝 Notes: {report['notes']}")
                    print(f"      🆔 ID: {report['id']}")
            else:
                print("No lab reports found.")
                
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # 3. Get specific lab report file data
    print("\n" + "=" * 50)
    print(f"\n3. Retrieving file data for report ID {stored_report_id}...")
    try:
        response = requests.post(f"{BASE_URL}/lab-reports/file/", json={
            "token": JWT_TOKEN,
            "report_id": stored_report_id
        })
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! File data retrieved:")
            print(f"   Report: {data['report_name']}")
            print(f"   File: {data['file_name']} ({data['file_type']})")
            print(f"   Size: {data['file_size_mb']} MB")
            print(f"   Is Image: {data['is_image']}")
            print(f"   Is PDF: {data['is_pdf']}")
            print(f"   Base64 data length: {len(data['file_data'])} characters")
            
            # Decode and display first few lines of the file content
            try:
                decoded_content = base64.b64decode(data['file_data']).decode('utf-8')
                lines = decoded_content.split('\n')[:10]  # First 10 lines
                print(f"\n   📄 File Content Preview:")
                for line in lines:
                    if line.strip():
                        print(f"      {line}")
                        
            except Exception as e:
                print(f"   Could not decode file content: {e}")
                
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def print_api_documentation():
    """Print API documentation for the lab report endpoints"""
    
    print("\n" + "=" * 60)
    print("📚 Lab Report API Documentation")
    print("=" * 60)
    
    print("\n🔗 1. Store Lab Report")
    print("POST /api/lab-reports/store/")
    print("Headers: Content-Type: application/json")
    print("\nRequest Body:")
    example_store = {
        "token": "your_jwt_token_here",
        "report_name": "Blood Test Report - September 2025",
        "report_type": "blood_test",
        "lab_name": "City Medical Laboratory",
        "doctor_name": "Dr. Sarah Smith",
        "report_date": "2025-09-25",
        "file_data": "base64_encoded_file_data_here",
        "file_name": "blood_test_report.pdf",
        "file_type": "pdf",
        "notes": "Optional notes about the report"
    }
    print(json.dumps(example_store, indent=2))
    
    print("\n🔗 2. Get All Lab Reports")
    print("POST /api/lab-reports/get/")
    print("Headers: Content-Type: application/json")
    print("\nRequest Body:")
    example_get_all = {
        "token": "your_jwt_token_here",
        "include_file_data": False  # Optional: set to true to include base64 data
    }
    print(json.dumps(example_get_all, indent=2))
    
    print("\n🔗 3. Get Specific Lab Report File")
    print("POST /api/lab-reports/file/")
    print("Headers: Content-Type: application/json")
    print("\nRequest Body:")
    example_get_file = {
        "token": "your_jwt_token_here",
        "report_id": 1
    }
    print(json.dumps(example_get_file, indent=2))
    
    print("\n📋 Field Descriptions:")
    print("• token: JWT authentication token (required)")
    print("• report_name: Descriptive name for the lab report (required)")
    print("• report_type: Type of lab report (required)")
    print("• lab_name: Name of the laboratory (optional)")
    print("• doctor_name: Name of the requesting doctor (optional)")
    print("• report_date: Date of the lab report in YYYY-MM-DD format (required)")
    print("• file_data: Base64 encoded file data (required)")
    print("• file_name: Original filename with extension (required)")
    print("• file_type: File extension without dot (required)")
    print("• notes: Additional notes about the report (optional)")
    
    print("\n🎯 Report Types:")
    print("• blood_test: Blood Test Reports")
    print("• urine_test: Urine Test Reports")
    print("• x_ray: X-Ray Images")
    print("• mri: MRI Scan Reports")
    print("• ct_scan: CT Scan Reports")
    print("• ultrasound: Ultrasound Reports")
    print("• ecg: ECG/EKG Reports")
    print("• pathology: Pathology Reports")
    print("• other: Other Types")
    
    print("\n💾 Supported File Types:")
    print("• Documents: pdf, doc, docx")
    print("• Images: jpg, jpeg, png, gif, bmp, tiff")
    print("• Maximum file size: 10MB")
    
    print("\n🔧 Base64 Encoding Example (Python):")
    print("""
import base64

# For text files
with open('report.txt', 'r') as file:
    content = file.read()
    base64_data = base64.b64encode(content.encode('utf-8')).decode('utf-8')

# For binary files (images, PDFs)
with open('report.pdf', 'rb') as file:
    content = file.read()
    base64_data = base64.b64encode(content).decode('utf-8')
    """)

def create_base64_from_file(file_path):
    """Helper function to create base64 from actual file"""
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            base64_data = base64.b64encode(content).decode('utf-8')
            return base64_data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

if __name__ == "__main__":
    # Print documentation
    print_api_documentation()
    
    print("\n" + "=" * 60)
    print("🚀 To test the API:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Register/login to get JWT token")
    print("3. Replace JWT_TOKEN in this script")
    print("4. Run: python test_lab_reports.py")
    
    print("\n💡 Tips:")
    print("• Use create_base64_from_file() to encode actual files")
    print("• Store base64 data in a variable before sending to API")
    print("• The API automatically validates base64 data and file size")
    print("• File data is excluded from list responses for performance")
    print("• Use the specific file endpoint to retrieve base64 data when needed")
    
    # Uncomment the line below and add your token to test
    # test_lab_report_api()