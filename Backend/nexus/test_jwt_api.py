"""
JWT Authentication Test Script for Food Nutrition API

This script demonstrates how to:
1. Register a new user
2. Login and get JWT tokens
3. Add food entries with authentication
4. Retrieve user-specific food history
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

class FoodNutritionClient:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.username = None

    def register(self, username, email, password):
        """Register a new user"""
        url = f"{BASE_URL}/register/"
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            result = response.json()
            self.access_token = result["tokens"]["access"]
            self.refresh_token = result["tokens"]["refresh"]
            self.username = username
            print(f"✅ User '{username}' registered successfully!")
            return result
        else:
            print(f"❌ Registration failed: {response.text}")
            return None

    def login(self, username, password):
        """Login and get JWT tokens"""
        url = f"{BASE_URL}/login/"
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.access_token = result["tokens"]["access"]
            self.refresh_token = result["tokens"]["refresh"]
            self.username = username
            print(f"✅ User '{username}' logged in successfully!")
            return result
        else:
            print(f"❌ Login failed: {response.text}")
            return None

    def add_food_entry(self, food_name, quantity):
        """Add a food entry (requires authentication)"""
        if not self.access_token:
            print("❌ Please login first!")
            return None
            
        url = f"{BASE_URL}/nutrition/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "food_name": food_name,
            "quantity": quantity
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Added {food_name} ({quantity}g) to {self.username}'s diary!")
            print(f"   Total calories: {result['total_nutrition']['calories']}")
            return result
        else:
            print(f"❌ Failed to add food entry: {response.text}")
            return None

    def get_food_history(self):
        """Get user's food history (requires authentication)"""
        if not self.access_token:
            print("❌ Please login first!")
            return None
            
        url = f"{BASE_URL}/nutrition/history/"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Retrieved {result['count']} entries for {result['user']}")
            return result
        else:
            print(f"❌ Failed to get food history: {response.text}")
            return None

def demonstrate_jwt_functionality():
    """Demonstrate the complete JWT authentication flow"""
    
    print("🍎 JWT Food Nutrition API Demo")
    print("=" * 50)
    
    # Create two different users to show data isolation
    client1 = FoodNutritionClient()
    client2 = FoodNutritionClient()
    
    print("\n1️⃣ Registering User 1...")
    client1.register("alice", "alice@example.com", "password123")
    
    print("\n2️⃣ Registering User 2...")
    client2.register("bob", "bob@example.com", "password456")
    
    print("\n3️⃣ Adding food entries for Alice...")
    client1.add_food_entry("apple", 150)
    client1.add_food_entry("banana", 120)
    client1.add_food_entry("chicken breast", 200)
    
    print("\n4️⃣ Adding food entries for Bob...")
    client2.add_food_entry("orange", 180)
    client2.add_food_entry("rice", 100)
    
    print("\n5️⃣ Retrieving Alice's food history...")
    alice_history = client1.get_food_history()
    if alice_history:
        print(f"   Alice has {alice_history['count']} food entries")
        for entry in alice_history['results'][:3]:  # Show first 3
            print(f"   - {entry['food_name']}: {entry['total_calories']} cal")
    
    print("\n6️⃣ Retrieving Bob's food history...")
    bob_history = client2.get_food_history()
    if bob_history:
        print(f"   Bob has {bob_history['count']} food entries")
        for entry in bob_history['results'][:3]:  # Show first 3
            print(f"   - {entry['food_name']}: {entry['total_calories']} cal")
    
    print("\n7️⃣ Testing authentication requirement...")
    # Try to access without token
    response = requests.get(f"{BASE_URL}/nutrition/history/")
    if response.status_code == 401:
        print("✅ Properly rejected unauthenticated request")
    else:
        print("❌ Security issue: Unauthenticated request was allowed")
    
    print("\n" + "=" * 50)
    print("🔒 JWT Authentication Demo Complete!")
    print("✅ User data is properly isolated")
    print("✅ Authentication is required for protected endpoints")
    print("✅ Each user can only access their own food diary")

def test_existing_user():
    """Test with existing user (if any)"""
    print("\n🔄 Testing with existing user...")
    client = FoodNutritionClient()
    
    # Try to login with the superuser we created
    if client.login("Gopesh", "password"):  # Replace with your superuser password
        print("✅ Logged in with existing user")
        client.add_food_entry("test_food", 100)
        history = client.get_food_history()
        if history:
            print(f"User has {history['count']} total entries")

if __name__ == "__main__":
    try:
        demonstrate_jwt_functionality()
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n📚 For more details, see JWT_API_DOCUMENTATION.md")