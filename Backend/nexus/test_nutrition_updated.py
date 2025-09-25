#!/usr/bin/env python3
"""
Test script for updated Nutrition API endpoint with time and meal_type fields
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_nutrition_api_with_new_format():
    """Test the nutrition endpoint with the new format including time and meal_type"""
    
    print("=== Testing Updated Nutrition API ===\n")
    
    # Step 1: Register/Login to get JWT token
    print("1. Getting JWT token...")
    login_data = {
        "username": "nutrition_test_user",
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
    
    # Step 2: Test with the new format
    print("2. Testing nutrition endpoint with new format...")
    nutrition_data = {
        "token": token,
        "food_name": "Apple",
        "quantity": 100,
        "unit": "g", 
        "time": "08:30",
        "meal_type": "breakfast"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/", 
                           json=nutrition_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        print("✅ Nutrition data retrieved and stored successfully")
        result = response.json()
        print("Response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Failed to get nutrition data: {response.status_code} - {response.text}")
        return
    
    print()
    
    # Step 3: Test with different meal type
    print("3. Testing with lunch meal type...")
    lunch_data = {
        "token": token,
        "food_name": "Banana",
        "quantity": 150,
        "unit": "g", 
        "time": "12:45",
        "meal_type": "lunch"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/", 
                           json=lunch_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        print("✅ Lunch nutrition data stored successfully")
        result = response.json()
        print(f"Food: {result['food_name']}")
        print(f"Time: {result['time']}")
        print(f"Meal Type: {result['meal_type']}")
        print(f"Total Calories: {result['total_nutrition']['calories']}")
    else:
        print(f"❌ Failed to store lunch data: {response.status_code} - {response.text}")
    
    print()
    
    # Step 4: Test without optional fields
    print("4. Testing without time and meal_type (should work)...")
    simple_data = {
        "token": token,
        "food_name": "Orange",
        "quantity": 80,
        "unit": "g"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/", 
                           json=simple_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        print("✅ Nutrition data without time/meal_type stored successfully")
        result = response.json()
        print(f"Food: {result['food_name']}")
        print(f"Time: {result['time']}")
        print(f"Meal Type: {result['meal_type']}")
    else:
        print(f"❌ Failed to store simple data: {response.status_code} - {response.text}")
    
    print()
    
    # Step 5: Test with different time formats
    print("5. Testing with evening snack...")
    snack_data = {
        "token": token,
        "food_name": "Almonds",
        "quantity": 30,
        "unit": "g", 
        "time": "19:15",
        "meal_type": "snack"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/", 
                           json=snack_data,
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        print("✅ Snack nutrition data stored successfully")
        result = response.json()
        print(f"Food: {result['food_name']}")
        print(f"Time: {result['time']}")
        print(f"Meal Type: {result['meal_type']}")
        print(f"Total Calories: {result['total_nutrition']['calories']}")
        print(f"Total Protein: {result['total_nutrition']['protein']}")
    else:
        print(f"❌ Failed to store snack data: {response.status_code} - {response.text}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    try:
        test_nutrition_api_with_new_format()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server. Make sure Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")