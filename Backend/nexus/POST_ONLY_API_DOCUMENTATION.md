# Food Nutrition API - POST Only Version

This documentation covers the updated Food Nutrition API where **ALL endpoints use POST requests**.

## Base URL
```
http://127.0.0.1:8000/api
```

## Authentication
All nutrition-related endpoints require JWT authentication:
```
Authorization: Bearer <your_jwt_token>
```

---

## 1. User Management

### Register User
**POST** `/register/`

**Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com", 
  "password": "secure_password"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### Login User  
**POST** `/login/`

**Body:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

---

## 2. Food Nutrition Endpoints

### Add Food Entry
**POST** `/nutrition/`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body:**
```json
{
  "food_name": "chicken breast",
  "quantity": 200
}
```

**Response:**
```json
{
  "food_name": "chicken breast",
  "quantity": 200,
  "unit": "grams",
  "nutrition_per_100g": {
    "calories": 165,
    "protein": 31,
    "carbohydrates": 0,
    "fat": 3.6,
    "fiber": 0,
    "sugar": 0
  },
  "total_nutrition": {
    "calories": 330,
    "protein": 62,
    "carbohydrates": 0,
    "fat": 7.2,
    "fiber": 0,
    "sugar": 0
  },
  "usda_food_name": "Chicken, broilers or fryers, breast, meat only, cooked, roasted",
  "stored_id": 15
}
```

### Get Nutrition History
**POST** `/nutrition/history/`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body:**
```json
{}
```

**Response:**
```json
{
  "user": "john_doe",
  "count": 10,
  "results": [
    {
      "id": 15,
      "food_name": "chicken breast",
      "quantity": 200,
      "total_calories": 330,
      "total_protein": 62,
      "total_carbs": 0,
      "total_fat": 7.2,
      "total_fiber": 0,
      "total_sugar": 0,
      "created_at": "2025-09-25T10:30:00Z"
    }
  ]
}
```

---

## 3. Nutrition Goals Management

### Get Nutrition Goals
**POST** `/nutrition/goals/`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body:**
```json
{
  "action": "get"
}
```

**Response:**
```json
{
  "id": 1,
  "daily_calories_goal": 2000.0,
  "daily_protein_goal": 50.0,
  "daily_carbs_goal": 250.0,
  "daily_fat_goal": 65.0,
  "daily_fiber_goal": 25.0,
  "daily_sugar_goal": 50.0,
  "created_at": "2025-09-25T09:00:00Z",
  "updated_at": "2025-09-25T09:00:00Z"
}
```

### Set/Update Nutrition Goals
**POST** `/nutrition/goals/`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body:**
```json
{
  "action": "set",
  "daily_calories_goal": 2200,
  "daily_protein_goal": 120,
  "daily_carbs_goal": 275,
  "daily_fat_goal": 70,
  "daily_fiber_goal": 30,
  "daily_sugar_goal": 40
}
```

**Response:**
```json
{
  "message": "Nutrition goals updated successfully",
  "goals": {
    "id": 1,
    "daily_calories_goal": 2200.0,
    "daily_protein_goal": 120.0,
    "daily_carbs_goal": 275.0,
    "daily_fat_goal": 70.0,
    "daily_fiber_goal": 30.0,
    "daily_sugar_goal": 40.0,
    "created_at": "2025-09-25T09:00:00Z",
    "updated_at": "2025-09-25T10:45:00Z"
  }
}
```

---

## 4. Daily Nutrition Summary

### Get Daily Summary
**POST** `/nutrition/summary/`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body (optional date):**
```json
{
  "date": "2025-09-25"
}
```

**Body (for today):**
```json
{}
```

**Response:**
```json
{
  "user": "john_doe",
  "summary": {
    "date": "2025-09-25",
    "consumed": {
      "calories": 1850.5,
      "protein": 98.2,
      "carbohydrates": 220.1,
      "fat": 62.8,
      "fiber": 28.5,
      "sugar": 35.2
    },
    "goals": {
      "calories": 2200.0,
      "protein": 120.0,
      "carbohydrates": 275.0,
      "fat": 70.0,
      "fiber": 30.0,
      "sugar": 40.0
    },
    "progress": {
      "calories_percentage": 84.1,
      "calories_remaining": 349.5,
      "protein_percentage": 81.8,
      "protein_remaining": 21.8,
      "carbohydrates_percentage": 80.0,
      "carbohydrates_remaining": 54.9,
      "fat_percentage": 89.7,
      "fat_remaining": 7.2,
      "fiber_percentage": 95.0,
      "fiber_remaining": 1.5,
      "sugar_percentage": 88.0,
      "sugar_remaining": 4.8
    },
    "entries_count": 6
  }
}
```

---

## JavaScript/Frontend Example

```javascript
class NutritionAPI {
  constructor(baseURL = 'http://127.0.0.1:8000/api') {
    this.baseURL = baseURL;
    this.accessToken = null;
  }

  async request(endpoint, data = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(this.accessToken && { 'Authorization': `Bearer ${this.accessToken}` })
      },
      body: JSON.stringify(data)
    });
    
    return await response.json();
  }

  async login(username, password) {
    const result = await this.request('/login/', { username, password });
    if (result.tokens) {
      this.accessToken = result.tokens.access;
    }
    return result;
  }

  async addFood(foodName, quantity) {
    return await this.request('/nutrition/', {
      food_name: foodName,
      quantity: quantity
    });
  }

  async getNutritionHistory() {
    return await this.request('/nutrition/history/', {});
  }

  async getNutritionGoals() {
    return await this.request('/nutrition/goals/', { action: 'get' });
  }

  async setNutritionGoals(goals) {
    return await this.request('/nutrition/goals/', {
      action: 'set',
      ...goals
    });
  }

  async getDailySummary(date = null) {
    const data = {};
    if (date) data.date = date;
    return await this.request('/nutrition/summary/', data);
  }
}

// Usage example
const api = new NutritionAPI();

// Login
await api.login('john_doe', 'password123');

// Add food
await api.addFood('chicken breast', 200);

// Get daily summary
const summary = await api.getDailySummary();
console.log('Daily progress:', summary.summary.progress);
```

---

## React Component Example

```jsx
import React, { useState, useEffect } from 'react';

const NutritionTracker = () => {
  const [summary, setSummary] = useState(null);
  const [api] = useState(new NutritionAPI());

  useEffect(() => {
    loadDailySummary();
  }, []);

  const loadDailySummary = async () => {
    try {
      const result = await api.getDailySummary();
      setSummary(result.summary);
    } catch (error) {
      console.error('Failed to load summary:', error);
    }
  };

  const addFood = async (foodName, quantity) => {
    try {
      await api.addFood(foodName, quantity);
      loadDailySummary(); // Refresh summary
    } catch (error) {
      console.error('Failed to add food:', error);
    }
  };

  if (!summary) return <div>Loading...</div>;

  return (
    <div className="nutrition-tracker">
      <h2>Daily Nutrition Progress</h2>
      
      {Object.entries(summary.consumed).map(([nutrient, consumed]) => {
        const goal = summary.goals[nutrient];
        const percentage = summary.progress[`${nutrient}_percentage`];
        
        return (
          <div key={nutrient} className="nutrient-progress">
            <span>{nutrient}: {consumed} / {goal}</span>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{width: `${Math.min(percentage, 100)}%`}}
              />
            </div>
            <span>{percentage}%</span>
          </div>
        );
      })}
      
      <button onClick={() => addFood('apple', 150)}>
        Add Apple (150g)
      </button>
    </div>
  );
};

export default NutritionTracker;
```

---

## Error Handling

All endpoints return consistent error formats:

```json
{
  "error": "Error message description",
  "details": "Additional technical details (when available)"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (invalid/missing token)
- `404`: Not Found 
- `500`: Internal Server Error
- `503`: Service Unavailable (external API issues)

---

## Key Changes in POST-Only Version

1. **All endpoints now use POST** - No more GET, PUT, or PATCH methods
2. **Data in request body** - All parameters (including optional ones) are sent in JSON body
3. **Nutrition goals endpoint** - Uses `action` field to determine get/set operation
4. **Daily summary endpoint** - Date passed in body instead of query parameter
5. **Nutrition history endpoint** - Requires empty JSON body `{}`

This design provides consistency and makes the API easier to integrate with frontend frameworks that prefer uniform HTTP methods.