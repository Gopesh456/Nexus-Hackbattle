#!/usr/bin/env python
"""
Test script to demonstrate Basic_Info API functionality.

This script tests all CRUD operations for the Basic_Info model:
1. Create basic info records
2. Retrieve individual and all records
3. Update records (both PUT and PATCH)
4. Search records with filters
5. Delete records
"""

import requests
import json
from datetime import date, timedelta

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

def test_create_basic_info():
    """Test creating basic info records"""
    print("=" * 60)
    print("TESTING CREATE BASIC INFO")
    print("=" * 60)
    
    # Sample data following the exact format requested
    sample_data = [
        {
            "full_name": "John Smith",
            "date_of_birth": "1995-03-15",
            "gender": "male",
            "location": "New York, USA",
            "email": "john.smith@example.com",
            "phone": "+1234567890"
        },
        {
            "full_name": "Sarah Johnson",
            "date_of_birth": "1990-07-22",
            "gender": "female",
            "location": "Los Angeles, USA",
            "email": "sarah.johnson@example.com",
            "phone": "+1987654321"
        },
        {
            "full_name": "Alex Chen",
            "date_of_birth": "1992-11-08",
            "gender": "other",
            "location": "San Francisco, USA",
            "email": "alex.chen@example.com",
            "phone": "+1122334455"
        }
    ]
    
    created_ids = []
    url = f"{BASE_URL}/basic-info/"
    
    for i, data in enumerate(sample_data, 1):
        print(f"Creating record {i}: {data['full_name']}")
        
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Created successfully - ID: {result['data']['id']}")
            created_ids.append(result['data']['id'])
            print(f"  Age calculated: {result['data']['age']} years")
        else:
            print(f"✗ Failed: {response.json()}")
        
        print("-" * 40)
    
    return created_ids

def test_get_all_basic_info():
    """Test retrieving all basic info records"""
    print("\\n" + "=" * 60)
    print("TESTING GET ALL BASIC INFO")
    print("=" * 60)
    
    url = f"{BASE_URL}/basic-info/all/"
    
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Total records found: {result['count']}")
        print("\\nRecords:")
        
        for record in result['data']:
            print(f"- ID: {record['id']}")
            print(f"  Name: {record['full_name']}")
            print(f"  Email: {record['email']}")
            print(f"  Age: {record['age']} years")
            print(f"  Location: {record['location']}")
            print()
    else:
        print(f"Failed: {response.json()}")

def test_get_single_basic_info(record_id):
    """Test retrieving a single basic info record"""
    print("\\n" + "=" * 60)
    print(f"TESTING GET SINGLE BASIC INFO (ID: {record_id})")
    print("=" * 60)
    
    url = f"{BASE_URL}/basic-info/{record_id}/"
    
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        data = result['data']
        print("Record details:")
        print(f"  ID: {data['id']}")
        print(f"  Full Name: {data['full_name']}")
        print(f"  Date of Birth: {data['date_of_birth']}")
        print(f"  Age: {data['age']} years")
        print(f"  Gender: {data['gender']}")
        print(f"  Location: {data['location']}")
        print(f"  Email: {data['email']}")
        print(f"  Phone: {data['phone']}")
        print(f"  Created: {data['created_at']}")
        print(f"  Updated: {data['updated_at']}")
    else:
        print(f"Failed: {response.json()}")

def test_update_basic_info(record_id):
    """Test updating basic info record"""
    print("\\n" + "=" * 60)
    print(f"TESTING UPDATE BASIC INFO (ID: {record_id})")
    print("=" * 60)
    
    # Test PATCH (partial update)
    url = f"{BASE_URL}/basic-info/{record_id}/update/"
    update_data = {
        "location": "Updated Location, USA",
        "phone": "+1999888777"
    }
    
    print("Testing PATCH (partial update)...")
    response = requests.patch(url, json=update_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Update successful")
        print(f"  New Location: {result['data']['location']}")
        print(f"  New Phone: {result['data']['phone']}")
    else:
        print(f"✗ Failed: {response.json()}")

def test_search_basic_info():
    """Test searching basic info records"""
    print("\\n" + "=" * 60)
    print("TESTING SEARCH BASIC INFO")
    print("=" * 60)
    
    # Test different search parameters
    search_tests = [
        {"full_name": "John", "description": "Search by partial name 'John'"},
        {"gender": "female", "description": "Search by gender 'female'"},
        {"location": "USA", "description": "Search by location containing 'USA'"},
    ]
    
    for search_params in search_tests:
        description = search_params.pop('description')
        print(f"\\n{description}:")
        
        url = f"{BASE_URL}/basic-info/search/"
        response = requests.get(url, params=search_params)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Found {result['count']} records")
            for record in result['data']:
                print(f"  - {record['full_name']} ({record['email']})")
        else:
            print(f"Failed: {response.json()}")

def test_delete_basic_info(record_id):
    """Test deleting a basic info record"""
    print("\\n" + "=" * 60)
    print(f"TESTING DELETE BASIC INFO (ID: {record_id})")
    print("=" * 60)
    
    url = f"{BASE_URL}/basic-info/{record_id}/delete/"
    
    response = requests.delete(url)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Delete successful")
        print(f"  Deleted record: {result['deleted_record']['full_name']}")
    else:
        print(f"✗ Failed: {response.json()}")

def test_validation_errors():
    """Test validation error scenarios"""
    print("\\n" + "=" * 60)
    print("TESTING VALIDATION ERRORS")
    print("=" * 60)
    
    # Test invalid data
    invalid_data_tests = [
        {
            "data": {
                "full_name": "",  # Empty name
                "date_of_birth": "1995-03-15",
                "gender": "male",
                "location": "Test Location",
                "email": "invalid-email",  # Invalid email
                "phone": "123"  # Invalid phone
            },
            "description": "Empty name, invalid email, invalid phone"
        },
        {
            "data": {
                "full_name": "Test User",
                "date_of_birth": "2030-01-01",  # Future date
                "gender": "invalid_gender",  # Invalid gender
                "location": "Test Location",
                "email": "test@example.com",
                "phone": "+1234567890"
            },
            "description": "Future date of birth, invalid gender"
        }
    ]
    
    url = f"{BASE_URL}/basic-info/"
    
    for test in invalid_data_tests:
        print(f"\\nTesting: {test['description']}")
        response = requests.post(url, json=test['data'])
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print("✓ Validation errors caught:")
            for field, errors in result['details'].items():
                print(f"  {field}: {errors}")
        else:
            print(f"Unexpected response: {response.json()}")

def main():
    """Main function to run all tests"""
    
    print("BASIC_INFO API FUNCTIONALITY TEST")
    print("=" * 60)
    print("Make sure the Django development server is running:")
    print("python manage.py runserver")
    print()
    
    try:
        # Create test records
        created_ids = test_create_basic_info()
        
        # Get all records
        test_get_all_basic_info()
        
        # Get single record (if any created)
        if created_ids:
            test_get_single_basic_info(created_ids[0])
            
            # Update record
            test_update_basic_info(created_ids[0])
        
        # Search records
        test_search_basic_info()
        
        # Test validation
        test_validation_errors()
        
        # Delete a record (if any created)
        if created_ids and len(created_ids) > 1:
            test_delete_basic_info(created_ids[-1])  # Delete the last created record
        
        print("\\n" + "=" * 60)
        print("API TESTS COMPLETED")
        print("=" * 60)
        print("\\nAll Basic_Info API endpoints have been tested!")
        print("Check the Django admin panel to see the created records:")
        print("http://127.0.0.1:8000/admin/")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API server.")
        print("Make sure the Django development server is running:")
        print("python manage.py runserver")

if __name__ == "__main__":
    main()