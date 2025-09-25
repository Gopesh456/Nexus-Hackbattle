#!/usr/bin/env python3
"""
Test script for nutrition edit and delete endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_nutrition_edit_delete():
    """Test the new nutrition edit and delete endpoints"""
    
    print("=== Testing Nutrition Edit & Delete Endpoints ===\n")
    
    # Step 1: Register/Login to get JWT token
    print("1. Getting JWT token...")
    login_data = {
        "username": "edit_delete_test_user",
        "password": "testpass123"
    }
    
    # Try registration first
    response = requests.post(f"{BASE_URL}/register/", 
                           json=login_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 201:
        print("✅ User registered successfully")
        result = response.json()
        token = result.get('tokens')
    else:
        # User might already exist, try login
        print("ℹ️  User might already exist, trying login...")
        response = requests.post(f"{BASE_URL}/login/", 
                               json=login_data,
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            print("✅ Login successful")
            result = response.json()
            token = result.get('tokens')
        else:
            print(f"❌ Registration/Login failed: {response.text}")
            return
    
    print(f"Token: {token[:50]}...\n")
    
    # Step 2: Add a nutrition item to test with
    print("2. Adding a nutrition item for testing...")
    initial_data = {
        "token": token,
        "food_name": "Apple",
        "quantity": 100,
        "unit": "g", 
        "time": "08:30",
        "meal_type": "breakfast"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/", 
                           json=initial_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        result = response.json()
        item_id = result.get('stored_id')
        print(f"✅ Initial nutrition item created with ID: {item_id}")
        print(f"Food: {result['food_name']}, Quantity: {result['quantity']}{result['unit']}")
        print(f"Time: {result['time']}, Meal: {result['meal_type']}")
        print(f"Calories: {result['total_nutrition']['calories']}")
    else:
        print(f"❌ Failed to create initial item: {response.status_code} - {response.text}")
        return
    
    print()
    
    # Step 3: Test editing the nutrition item
    print("3. Testing edit nutrition item...")
    edit_data = {
        "token": token,
        "item_id": item_id,
        "food_name": "Large Red Apple",
        "quantity": 150,
        "unit": "g",
        "time": "09:00",
        "meal_type": "breakfast"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/edit/", 
                           json=edit_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Nutrition item edited successfully")
        print(f"Updated Food: {result['food_name']}")
        print(f"Updated Quantity: {result['quantity']}{result['unit']}")
        print(f"Updated Time: {result['time']}")
        print(f"Updated Calories: {result['total_nutrition']['calories']}")
        print(f"Message: {result['message']}")
    else:
        print(f"❌ Failed to edit nutrition item: {response.status_code} - {response.text}")
        return
    
    print()
    
    # Step 4: Add another item for delete testing
    print("4. Adding another item for delete testing...")
    second_data = {
        "token": token,
        "food_name": "Banana",
        "quantity": 120,
        "unit": "g", 
        "time": "14:30",
        "meal_type": "snack"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/", 
                           json=second_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        result = response.json()
        second_item_id = result.get('stored_id')
        print(f"✅ Second nutrition item created with ID: {second_item_id}")
        print(f"Food: {result['food_name']}, Time: {result['time']}, Meal: {result['meal_type']}")
    else:
        print(f"❌ Failed to create second item: {response.status_code} - {response.text}")
        return
    
    print()
    
    # Step 5: Test deleting the second item
    print("5. Testing delete nutrition item...")
    delete_data = {
        "token": token,
        "item_id": second_item_id
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/delete/", 
                           json=delete_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Nutrition item deleted successfully")
        print(f"Message: {result['message']}")
        print(f"Deleted Item: {result['deleted_item']['food_name']} - {result['deleted_item']['quantity']}{result['deleted_item']['unit']}")
    else:
        print(f"❌ Failed to delete nutrition item: {response.status_code} - {response.text}")
    
    print()
    
    # Step 6: Test error cases
    print("6. Testing error cases...")
    
    # Try to edit non-existent item
    print("6a. Testing edit with invalid item_id...")
    invalid_edit = {
        "token": token,
        "item_id": 99999,
        "food_name": "Non-existent",
        "quantity": 50,
        "unit": "g"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/edit/", 
                           json=invalid_edit,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 404:
        print("✅ Correctly returned 404 for non-existent item")
    else:
        print(f"❌ Expected 404, got {response.status_code}")
    
    # Try to delete non-existent item
    print("6b. Testing delete with invalid item_id...")
    invalid_delete = {
        "token": token,
        "item_id": 99999
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/delete/", 
                           json=invalid_delete,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 404:
        print("✅ Correctly returned 404 for non-existent item")
    else:
        print(f"❌ Expected 404, got {response.status_code}")
    
    # Try edit without item_id
    print("6c. Testing edit without item_id...")
    no_id_edit = {
        "token": token,
        "food_name": "Test",
        "quantity": 50,
        "unit": "g"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/edit/", 
                           json=no_id_edit,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 400:
        print("✅ Correctly returned 400 for missing item_id")
    else:
        print(f"❌ Expected 400, got {response.status_code}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    try:
        test_nutrition_edit_delete()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server. Make sure Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")