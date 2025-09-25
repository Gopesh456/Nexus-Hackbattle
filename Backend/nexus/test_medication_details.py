#!/usr/bin/env python3
"""
Test script for Medication Details API endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_medication_details_api():
    """Test the medication details endpoints"""
    
    print("=== Testing Medication Details API ===\n")
    
    # Step 1: Register a test user
    print("1. Registering test user...")
    register_data = {
        "username": "med_test_user",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/register/", 
                           json=register_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 201:
        print("✅ User registered successfully")
        register_result = response.json()
        token = register_result.get('tokens')
    else:
        # User might already exist, try login
        print("ℹ️  User might already exist, trying login...")
        response = requests.post(f"{BASE_URL}/login/", 
                               json=register_data,
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            print("✅ Login successful")
            register_result = response.json()
            token = register_result.get('tokens')
        else:
            print(f"❌ Registration/Login failed: {response.text}")
            return
    
    print(f"Token: {token[:50]}...\n")
    
    # Step 2: Store medication details
    print("2. Storing medication details...")
    medication_data = {
        "token": token,
        "Medicine_name": "Metformin",
        "Frequency": "Twice daily",
        "Medical_Condition": "Type 2 Diabetes",
        "No_of_pills": "1 tablet",
        "next_order_data": "2025-10-15",
        "meds_reminder": "Take with meals to reduce stomach upset"
    }
    
    response = requests.post(f"{BASE_URL}/medication-details/store/", 
                           json=medication_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        print("✅ Medication details stored successfully")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Failed to store medication details: {response.status_code} - {response.text}")
        return
    
    print()
    
    # Step 3: Retrieve medication details
    print("3. Retrieving medication details...")
    get_data = {
        "token": token
    }
    
    response = requests.post(f"{BASE_URL}/medication-details/get/", 
                           json=get_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        print("✅ Medication details retrieved successfully")
        result = response.json()
        print("Retrieved data:")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Failed to retrieve medication details: {response.status_code} - {response.text}")
        return
    
    print()
    
    # Step 4: Update medication details
    print("4. Updating medication details...")
    updated_data = {
        "token": token,
        "Medicine_name": "Lisinopril",
        "Frequency": "Once daily",
        "Medical_Condition": "High Blood Pressure",
        "No_of_pills": "1 tablet (10mg)",
        "next_order_data": "2025-11-20",
        "meds_reminder": "Take in the morning, avoid potassium supplements"
    }
    
    response = requests.post(f"{BASE_URL}/medication-details/store/", 
                           json=updated_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        print("✅ Medication details updated successfully")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Failed to update medication details: {response.status_code} - {response.text}")
        return
    
    print()
    
    # Step 5: Retrieve updated data
    print("5. Retrieving updated medication details...")
    response = requests.post(f"{BASE_URL}/medication-details/get/", 
                           json=get_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        print("✅ Updated medication details retrieved successfully")
        result = response.json()
        print("Updated data:")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Failed to retrieve updated medication details: {response.status_code} - {response.text}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    try:
        test_medication_details_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server. Make sure Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")