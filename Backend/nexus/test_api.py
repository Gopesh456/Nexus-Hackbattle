"""
Sample API Usage and Testing Script

This script demonstrates how to use the food nutrition endpoint.
"""

import requests
import json

# API Base URL (update this if your Django server runs on a different port)
BASE_URL = "http://127.0.0.1:8000/api"

def test_food_nutrition_api():
    """Test the food nutrition endpoint"""
    
    # Sample food data
    food_data = {
        "food_name": "apple",
        "quantity": 150  # in grams
    }
    
    # Make POST request to nutrition endpoint
    url = f"{BASE_URL}/nutrition/"
    
    try:
        response = requests.post(url, json=food_data)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! Food nutrition data retrieved:")
            print(f"Food: {data['food_name']}")
            print(f"Quantity: {data['quantity']}g")
            print(f"USDA Food Name: {data['usda_food_name']}")
            print("\nNutrition per 100g:")
            for nutrient, value in data['nutrition_per_100g'].items():
                print(f"  {nutrient}: {value}")
            print("\nTotal nutrition for your quantity:")
            for nutrient, value in data['total_nutrition'].items():
                print(f"  {nutrient}: {value}")
            print(f"\nStored with ID: {data['stored_id']}")
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure your Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_nutrition_history_api():
    """Test the nutrition history endpoint"""
    
    url = f"{BASE_URL}/nutrition/history/"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data['count']} nutrition records")
            
            if data['results']:
                print("\nRecent nutrition entries:")
                for record in data['results'][:5]:  # Show first 5
                    print(f"- {record['food_name']} ({record['quantity']}g): {record['total_calories']} kcal")
            else:
                print("No nutrition records found.")
                
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure your Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("🍎 Testing Food Nutrition API")
    print("=" * 50)
    
    print("\n1. Testing food nutrition endpoint:")
    test_food_nutrition_api()
    
    print("\n" + "=" * 50)
    print("\n2. Testing nutrition history endpoint:")
    test_nutrition_history_api()
    
    print("\n" + "=" * 50)
    print("\n🔗 Frontend Integration Guide:")
    print("POST /api/nutrition/")
    print("Body: {\"food_name\": \"apple\", \"quantity\": 150}")
    print("Response: Complete nutrition data + stored in database")
    print("\nGET /api/nutrition/history/")
    print("Response: List of all stored nutrition records")