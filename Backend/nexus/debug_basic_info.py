#!/usr/bin/env python3
"""
Debug script to test various scenarios for the Basic_Info API endpoint.
This will help identify what causes 400 errors vs successful requests.
"""

import requests
import json
from datetime import date, timedelta

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_scenario(name, data, expected_status=None):
    """Test a specific scenario and report results"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/basic-info/",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ SUCCESS: Record created!")
            result = response.json()
            print(f"Created ID: {result['data']['id']}")
        elif response.status_code == 400:
            print("❌ BAD REQUEST: Validation failed")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('error', 'Unknown error')}")
                if 'details' in error_data:
                    print("Validation Errors:")
                    for field, errors in error_data['details'].items():
                        print(f"  - {field}: {', '.join(errors)}")
            except:
                print(f"Raw response: {response.text}")
        else:
            print(f"❓ UNEXPECTED STATUS: {response.status_code}")
            print(f"Response: {response.text}")
            
        if expected_status and response.status_code != expected_status:
            print(f"⚠️  Expected {expected_status}, got {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Django server not running")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def main():
    print("Basic Info API Debug Test")
    print("="*60)
    
    # Test 1: Valid complete data
    test_scenario(
        "Valid Complete Data",
        {
            "full_name": "Alice Johnson",
            "date_of_birth": "1992-03-15",
            "gender": "female",
            "location": "Los Angeles, CA",
            "email": "alice.johnson@example.com",
            "phone": "+1555123456"
        },
        expected_status=201
    )
    
    # Test 2: Missing required fields
    test_scenario(
        "Missing Required Fields",
        {
            "full_name": "Bob Smith"
        },
        expected_status=400
    )
    
    # Test 3: Invalid email format
    test_scenario(
        "Invalid Email Format",
        {
            "full_name": "Charlie Brown",
            "date_of_birth": "1988-07-20",
            "gender": "male",
            "location": "Chicago, IL",
            "email": "invalid-email",
            "phone": "+1555987654"
        },
        expected_status=400
    )
    
    # Test 4: Invalid phone format
    test_scenario(
        "Invalid Phone Format",
        {
            "full_name": "Diana Prince",
            "date_of_birth": "1995-11-10",
            "gender": "female",
            "location": "Seattle, WA",
            "email": "diana.prince@example.com",
            "phone": "123"  # Too short
        },
        expected_status=400
    )
    
    # Test 5: Invalid gender
    test_scenario(
        "Invalid Gender",
        {
            "full_name": "Eve Wilson",
            "date_of_birth": "1990-12-25",
            "gender": "invalid_gender",
            "location": "Miami, FL",
            "email": "eve.wilson@example.com",
            "phone": "+1555555555"
        },
        expected_status=400
    )
    
    # Test 6: Future date of birth
    test_scenario(
        "Future Date of Birth",
        {
            "full_name": "Future Person",
            "date_of_birth": "2030-01-01",
            "gender": "other",
            "location": "Future City",
            "email": "future@example.com",
            "phone": "+1555000000"
        },
        expected_status=400
    )
    
    # Test 7: Duplicate email
    test_scenario(
        "Duplicate Email (should fail)",
        {
            "full_name": "Duplicate User",
            "date_of_birth": "1985-06-15",
            "gender": "male",
            "location": "Denver, CO",
            "email": "alice.johnson@example.com",  # Same as first test
            "phone": "+1555111111"
        },
        expected_status=400
    )
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print("✅ 201 = Success: Valid data was accepted")
    print("❌ 400 = Bad Request: Invalid/missing data was rejected")
    print("🔍 Check the validation errors above to understand what's wrong")

if __name__ == "__main__":
    main()
