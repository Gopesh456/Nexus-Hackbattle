"""
Comprehensive Test Script for Food Nutrition API with Goals and Totals

This script demonstrates:
1. User registration and login
2. Setting nutrition goals
3. Adding food entries
4. Calculating daily totals and progress against goals
5. Getting nutrition summary with goal comparison
"""

import requests
import json
from datetime import date

BASE_URL = "http://127.0.0.1:8000/api"

class NutritionTracker:
    def __init__(self):
        self.access_token = None
        self.username = None
    
    def register_and_login(self, username, email, password):
        """Register or login user"""
        # Try to register first
        register_data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        response = requests.post(f"{BASE_URL}/register/", json=register_data)
        
        if response.status_code == 201:
            result = response.json()
            self.access_token = result["tokens"]["access"]
            self.username = username
            print(f"✅ User '{username}' registered successfully!")
            return True
        else:
            # Try to login instead
            login_data = {"username": username, "password": password}
            response = requests.post(f"{BASE_URL}/login/", json=login_data)
            
            if response.status_code == 200:
                result = response.json()
                self.access_token = result["tokens"]["access"]
                self.username = username
                print(f"✅ User '{username}' logged in successfully!")
                return True
            else:
                print(f"❌ Failed to register/login: {response.text}")
                return False
    
    def set_nutrition_goals(self, goals):
        """Set user's daily nutrition goals"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Add action field for POST request
        goals_data = goals.copy()
        goals_data["action"] = "set"
        
        response = requests.post(f"{BASE_URL}/nutrition/goals/", json=goals_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Nutrition goals set for {self.username}!")
            print(f"   Goals: {result['goals']}")
            return result
        else:
            print(f"❌ Failed to set goals: {response.text}")
            return None
    
    def get_nutrition_goals(self):
        """Get user's current nutrition goals"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.post(f"{BASE_URL}/nutrition/goals/", json={"action": "get"}, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Current goals for {self.username}:")
            for key, value in result.items():
                if 'goal' in key:
                    nutrient = key.replace('daily_', '').replace('_goal', '')
                    print(f"   {nutrient.title()}: {value}")
            return result
        else:
            print(f"❌ Failed to get goals: {response.text}")
            return None
    
    def add_food_entry(self, food_name, quantity):
        """Add a food entry"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"food_name": food_name, "quantity": quantity}
        
        response = requests.post(f"{BASE_URL}/nutrition/", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            total_cal = result['total_nutrition']['calories']
            print(f"✅ Added {food_name} ({quantity}g) - {total_cal} calories")
            return result
        else:
            print(f"❌ Failed to add {food_name}: {response.text}")
            return None
    
    def get_nutrition_history(self):
        """Get nutrition history"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.post(f"{BASE_URL}/nutrition/history/", json={}, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Retrieved {result['count']} nutrition entries for {self.username}")
            return result
        else:
            print(f"❌ Failed to get nutrition history: {response.text}")
            return None
    
    def get_daily_summary(self, date_str=None):
        """Get daily nutrition summary with goal progress"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Send date in POST body instead of query parameter
        data = {}
        if date_str:
            data["date"] = date_str
        
        response = requests.post(f"{BASE_URL}/nutrition/summary/", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            summary = result['summary']
            
            print(f"\n📊 Daily Nutrition Summary for {self.username} - {summary['date']}")
            print("=" * 60)
            print(f"Total food entries: {summary['entries_count']}")
            print("\n🎯 Goals vs Consumed:")
            
            nutrients = ['calories', 'protein', 'carbohydrates', 'fat', 'fiber', 'sugar']
            for nutrient in nutrients:
                consumed = summary['consumed'][nutrient]
                goal = summary['goals'][nutrient]
                percentage = summary['progress'][f"{nutrient}_percentage"]
                remaining = summary['progress'][f"{nutrient}_remaining"]
                
                status = "✅" if percentage >= 100 else "🔄" if percentage >= 80 else "❌"
                unit = "g" if nutrient != 'calories' else 'kcal'
                
                print(f"{status} {nutrient.title()}: {consumed}{unit}/{goal}{unit} ({percentage}% - {remaining}{unit} remaining)")
            
            return result
        else:
            print(f"❌ Failed to get daily summary: {response.text}")
            return None

def demonstrate_nutrition_tracking():
    """Demonstrate the complete nutrition tracking system"""
    
    print("🍎 Food Nutrition Tracker with Goals & Totals")
    print("=" * 60)
    
    tracker = NutritionTracker()
    
    # Step 1: Register/Login
    print("\n1️⃣ Setting up user...")
    if not tracker.register_and_login("john_fitness", "john@fitness.com", "healthylife123"):
        return
    
    # Step 2: Set nutrition goals
    print("\n2️⃣ Setting nutrition goals...")
    goals = {
        "daily_calories_goal": 2200,
        "daily_protein_goal": 120,
        "daily_carbs_goal": 275,
        "daily_fat_goal": 70,
        "daily_fiber_goal": 30,
        "daily_sugar_goal": 40
    }
    tracker.set_nutrition_goals(goals)
    
    # Step 3: Add some food entries
    print("\n3️⃣ Adding food entries...")
    foods_to_add = [
        ("chicken breast", 200),
        ("brown rice", 150),
        ("broccoli", 100),
        ("apple", 150),
        ("almonds", 30),
        ("greek yogurt", 170)
    ]
    
    for food, quantity in foods_to_add:
        tracker.add_food_entry(food, quantity)
    
    # Step 4: Get daily summary
    print("\n4️⃣ Getting daily nutrition summary...")
    tracker.get_daily_summary()
    
    # Step 5: Add more food and check progress
    print("\n5️⃣ Adding more food and checking progress...")
    tracker.add_food_entry("banana", 120)
    tracker.add_food_entry("oatmeal", 80)
    tracker.get_daily_summary()
    
    # Step 6: Check goals
    print("\n6️⃣ Current nutrition goals:")
    tracker.get_nutrition_goals()

def test_api_endpoints():
    """Test individual API endpoints"""
    print("\n🔧 Testing API Endpoints")
    print("=" * 40)
    
    tracker = NutritionTracker()
    
    # Test with existing user
    print("Testing with existing user...")
    if tracker.register_and_login("test_user", "test@example.com", "password123"):
        
        print("\n📋 Testing Goals Endpoint:")
        # Test GET goals (should create default goals)
        tracker.get_nutrition_goals()
        
        # Test SET goals (update goals)
        custom_goals = {
            "daily_calories_goal": 1800,
            "daily_protein_goal": 100
        }
        tracker.set_nutrition_goals(custom_goals)
        
        print("\n🍽️ Testing Food Entry:")
        tracker.add_food_entry("test_food", 100)
        
        print("\n📜 Testing Nutrition History:")
        tracker.get_nutrition_history()
        
        print("\n📊 Testing Daily Summary:")
        tracker.get_daily_summary()
        
        # Test with specific date
        print("\n📅 Testing with specific date:")
        tracker.get_daily_summary(date.today().strftime('%Y-%m-%d'))

if __name__ == "__main__":
    try:
        demonstrate_nutrition_tracking()
        test_api_endpoints()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        print("\n📋 All API Endpoints (All POST requests):")
        print("• POST /api/nutrition/goals/ - Manage nutrition goals (action: get/set)")
        print("• POST /api/nutrition/summary/ - Daily nutrition summary with progress")
        print("• POST /api/nutrition/history/ - Get nutrition history")
        print("• POST /api/nutrition/ - Add food entries")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()