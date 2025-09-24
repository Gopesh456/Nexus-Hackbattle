"""
Quick test to verify the daily summary works with the correct date
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_daily_summary_with_correct_date():
    # Login as john_fitness
    login_data = {"username": "john_fitness", "password": "healthylife123"}
    login_response = requests.post(f"{BASE_URL}/login/", json=login_data)
    
    if login_response.status_code == 200:
        access_token = login_response.json()["tokens"]["access"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        print("🧪 Testing daily summary with yesterday's date (2025-09-24)...")
        
        # Get summary for 2025-09-24 (when the food entries were created)
        summary_data = {"date": "2025-09-24"}
        response = requests.post(f"{BASE_URL}/nutrition/summary/", json=summary_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            summary = result['summary']
            
            print(f"✅ Daily Nutrition Summary for {summary['date']}")
            print("=" * 50)
            print(f"Total food entries: {summary['entries_count']}")
            
            nutrients = ['calories', 'protein', 'carbohydrates', 'fat', 'fiber', 'sugar']
            for nutrient in nutrients:
                consumed = summary['consumed'][nutrient]
                goal = summary['goals'][nutrient]
                percentage = summary['progress'][f"{nutrient}_percentage"]
                
                status = "✅" if percentage >= 100 else "🔄" if percentage >= 80 else "❌"
                unit = "g" if nutrient != 'calories' else 'kcal'
                print(f"{status} {nutrient.title()}: {consumed}{unit}/{goal}{unit} ({percentage}%)")
            
            print("\n🎉 Daily summary working perfectly with POST request!")
        else:
            print(f"❌ Failed: {response.text}")
    else:
        print(f"❌ Login failed: {login_response.text}")

if __name__ == "__main__":
    try:
        test_daily_summary_with_correct_date()
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running.")
    except Exception as e:
        print(f"❌ Error: {e}")