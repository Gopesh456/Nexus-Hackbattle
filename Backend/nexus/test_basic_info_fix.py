#!/usr/bin/env python3
"""
Test script to verify the Basic_Info API endpoint is working after fixing the missing model.
"""

import requests
import json
from datetime import date, timedelta

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_basic_info_endpoint():
    """Test the basic-info endpoint with valid data"""
    
    # Test data
    test_data = {
        "full_name": "John Doe",
        "date_of_birth": "1995-05-15",
        "gender": "male",
        "location": "New York, USA",
        "email": "john.doe@example.com",
        "phone": "+1234567890"
    }
    
    print("Testing Basic Info API endpoint...")
    print(f"URL: {BASE_URL}/basic-info/")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/basic-info/",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            print("✅ SUCCESS: Basic Info created successfully!")
            print(f"Response Data: {json.dumps(response.json(), indent=2)}")
        elif response.status_code == 400:
            print("❌ BAD REQUEST: There's still an issue with the endpoint")
            print(f"Error Details: {response.text}")
        else:
            print(f"❌ UNEXPECTED STATUS: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Make sure the Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def test_get_basic_info():
    """Test getting all basic info records"""
    
    print("\n" + "="*50)
    print("Testing GET all basic info records...")
    
    try:
        response = requests.get(f"{BASE_URL}/basic-info/all/")
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS: Retrieved basic info records!")
            print(f"Count: {data.get('count', 0)}")
            print(f"Records: {json.dumps(data.get('data', []), indent=2)}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Make sure the Django server is running")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    print("Basic Info API Endpoint Test")
    print("="*50)
    
    test_basic_info_endpoint()
    test_get_basic_info()
    
    print("\n" + "="*50)
    print("Test completed!")
