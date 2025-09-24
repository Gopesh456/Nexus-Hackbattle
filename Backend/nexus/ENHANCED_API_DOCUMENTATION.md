# Food Nutrition API with Goals & Daily Totals - Complete Documentation

## Overview
Enhanced food nutrition API with user-specific goals, daily totals calculation, and progress tracking. Users can set nutrition goals and monitor their daily progress against these targets.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
All endpoints require JWT authentication except registration and login:
```
Authorization: Bearer <your_jwt_token>
```

---

## 📊 New Features

### 🎯 Nutrition Goals
Users can set and manage their daily nutrition goals for calories and macronutrients.

### 📈 Daily Totals & Progress
Automatic calculation of daily nutrition totals with progress tracking against goals.

### 📋 Daily Summary
Comprehensive daily nutrition summary showing consumed vs goals with percentage progress.

---

## 🔐 Authentication Endpoints

### Register User
**POST** `/register/`

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securePassword123"
}
```

### Login User
**POST** `/login/`

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "securePassword123"
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

## 🍽️ Food Entry Endpoints

### Add Food Entry
**POST** `/nutrition/`

Add food entry and get nutrition data (stores for authenticated user).

**Headers:**
```
Authorization: Bearer <jwt_access_token>
Content-Type: application/json
```

**Request Body:**
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
        "calories": 165.0,
        "protein": 31.0,
        "carbohydrates": 0.0,
        "fat": 3.6,
        "fiber": 0.0,
        "sugar": 0.0
    },
    "total_nutrition": {
        "calories": 330.0,
        "protein": 62.0,
        "carbohydrates": 0.0,
        "fat": 7.2,
        "fiber": 0.0,
        "sugar": 0.0
    },
    "usda_food_name": "Chicken, breast, meat only, cooked, roasted",
    "stored_id": 1
}
```

### Get Food History
**GET** `/nutrition/history/`

Retrieve user's food diary history.

**Headers:**
```
Authorization: Bearer <jwt_access_token>
```

**Response:**
```json
{
    "user": "john_doe",
    "count": 5,
    "results": [
        {
            "id": 1,
            "username": "john_doe",
            "food_name": "chicken breast",
            "quantity": 200.0,
            "total_calories": 330.0,
            "total_protein": 62.0,
            "created_at": "2025-09-24T23:30:00Z"
        }
    ]
}
```

---

## 🎯 Nutrition Goals Endpoints

### Get Nutrition Goals
**GET** `/nutrition/goals/`

Retrieve user's nutrition goals (creates default goals if none exist).

**Headers:**
```
Authorization: Bearer <jwt_access_token>
```

**Response:**
```json
{
    "id": 1,
    "username": "john_doe",
    "daily_calories_goal": 2000.0,
    "daily_protein_goal": 50.0,
    "daily_carbs_goal": 250.0,
    "daily_fat_goal": 65.0,
    "daily_fiber_goal": 25.0,
    "daily_sugar_goal": 50.0,
    "created_at": "2025-09-24T23:30:00Z",
    "updated_at": "2025-09-24T23:30:00Z"
}
```

### Set/Update Nutrition Goals
**PUT** `/nutrition/goals/` or **POST** `/nutrition/goals/`

Set or update user's nutrition goals.

**Headers:**
```
Authorization: Bearer <jwt_access_token>
Content-Type: application/json
```

**Request Body (partial updates allowed):**
```json
{
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
        "username": "john_doe",
        "daily_calories_goal": 2200.0,
        "daily_protein_goal": 120.0,
        "daily_carbs_goal": 275.0,
        "daily_fat_goal": 70.0,
        "daily_fiber_goal": 30.0,
        "daily_sugar_goal": 40.0,
        "updated_at": "2025-09-24T23:45:00Z"
    }
}
```

---

## 📊 Daily Summary Endpoint

### Get Daily Nutrition Summary
**GET** `/nutrition/summary/`

Get comprehensive daily nutrition summary with goal progress.

**Headers:**
```
Authorization: Bearer <jwt_access_token>
```

**Query Parameters:**
- `date` (optional): Date in YYYY-MM-DD format. Defaults to today.

**Example:**
```
GET /nutrition/summary/?date=2025-09-24
```

**Response:**
```json
{
    "user": "john_doe",
    "summary": {
        "date": "2025-09-24",
        "consumed": {
            "calories": 1850.5,
            "protein": 98.2,
            "carbohydrates": 220.8,
            "fat": 62.1,
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
            "carbohydrates_percentage": 80.3,
            "carbohydrates_remaining": 54.2,
            "fat_percentage": 88.7,
            "fat_remaining": 7.9,
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

## 💻 Frontend Integration Examples

### Complete Nutrition Tracker Class
```javascript
class NutritionTracker {
    constructor() {
        this.baseURL = 'http://127.0.0.1:8000/api';
        this.accessToken = localStorage.getItem('access_token');
    }

    async login(username, password) {
        const response = await fetch(`${this.baseURL}/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            this.accessToken = data.tokens.access;
            localStorage.setItem('access_token', data.tokens.access);
            return data;
        }
        throw new Error('Login failed');
    }

    // Set nutrition goals
    async setNutritionGoals(goals) {
        const response = await fetch(`${this.baseURL}/nutrition/goals/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.accessToken}`
            },
            body: JSON.stringify(goals)
        });
        return await response.json();
    }

    // Get nutrition goals
    async getNutritionGoals() {
        const response = await fetch(`${this.baseURL}/nutrition/goals/`, {
            headers: { 'Authorization': `Bearer ${this.accessToken}` }
        });
        return await response.json();
    }

    // Add food entry
    async addFoodEntry(foodName, quantity) {
        const response = await fetch(`${this.baseURL}/nutrition/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.accessToken}`
            },
            body: JSON.stringify({
                food_name: foodName,
                quantity: quantity
            })
        });
        return await response.json();
    }

    // Get daily summary
    async getDailySummary(date = null) {
        let url = `${this.baseURL}/nutrition/summary/`;
        if (date) url += `?date=${date}`;
        
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${this.accessToken}` }
        });
        return await response.json();
    }
}

// Usage Example
const tracker = new NutritionTracker();

// Set goals
await tracker.setNutritionGoals({
    daily_calories_goal: 2200,
    daily_protein_goal: 120,
    daily_carbs_goal: 275
});

// Add food
await tracker.addFoodEntry('chicken breast', 200);

// Get daily progress
const summary = await tracker.getDailySummary();
console.log(`Calories: ${summary.summary.consumed.calories}/${summary.summary.goals.calories}`);
```

### React Component Example
```jsx
import React, { useState, useEffect } from 'react';

function NutritionDashboard() {
    const [summary, setSummary] = useState(null);
    const [goals, setGoals] = useState(null);

    useEffect(() => {
        fetchDailySummary();
        fetchGoals();
    }, []);

    const fetchDailySummary = async () => {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://127.0.0.1:8000/api/nutrition/summary/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        setSummary(data.summary);
    };

    const fetchGoals = async () => {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://127.0.0.1:8000/api/nutrition/goals/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        setGoals(data);
    };

    const NutrientProgress = ({ nutrient, consumed, goal, unit }) => {
        const percentage = goal > 0 ? (consumed / goal) * 100 : 0;
        const remaining = Math.max(0, goal - consumed);
        
        return (
            <div className="nutrient-progress">
                <h4>{nutrient.charAt(0).toUpperCase() + nutrient.slice(1)}</h4>
                <div className="progress-bar">
                    <div 
                        className="progress-fill" 
                        style={{ width: `${Math.min(percentage, 100)}%` }}
                    />
                </div>
                <p>{consumed.toFixed(1)}{unit} / {goal}{unit} ({percentage.toFixed(1)}%)</p>
                <p>Remaining: {remaining.toFixed(1)}{unit}</p>
            </div>
        );
    };

    if (!summary || !goals) return <div>Loading...</div>;

    return (
        <div className="nutrition-dashboard">
            <h2>Daily Nutrition Progress</h2>
            <p>Date: {summary.date}</p>
            <p>Food entries: {summary.entries_count}</p>
            
            <div className="nutrients-grid">
                <NutrientProgress 
                    nutrient="calories" 
                    consumed={summary.consumed.calories} 
                    goal={summary.goals.calories} 
                    unit="kcal" 
                />
                <NutrientProgress 
                    nutrient="protein" 
                    consumed={summary.consumed.protein} 
                    goal={summary.goals.protein} 
                    unit="g" 
                />
                <NutrientProgress 
                    nutrient="carbohydrates" 
                    consumed={summary.consumed.carbohydrates} 
                    goal={summary.goals.carbohydrates} 
                    unit="g" 
                />
                <NutrientProgress 
                    nutrient="fat" 
                    consumed={summary.consumed.fat} 
                    goal={summary.goals.fat} 
                    unit="g" 
                />
            </div>
        </div>
    );
}
```

---

## 📋 API Endpoints Summary

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| POST | `/register/` | Register new user | ❌ |
| POST | `/login/` | Login user | ❌ |
| POST | `/nutrition/` | Add food entry | ✅ |
| GET | `/nutrition/history/` | Get food history | ✅ |
| GET | `/nutrition/goals/` | Get nutrition goals | ✅ |
| PUT/POST | `/nutrition/goals/` | Set/update goals | ✅ |
| GET | `/nutrition/summary/` | Daily summary & progress | ✅ |
| POST | `/token/refresh/` | Refresh JWT token | ✅ |

---

## 🧪 Testing

### Run comprehensive test
```bash
python test_nutrition_goals.py
```

### Test individual features
```bash
# Test JWT authentication
python test_jwt_api.py

# Test basic functionality
python test_api.py
```

---

## 🔐 Security & Performance

- **JWT Authentication**: Secure user authentication
- **User Data Isolation**: Each user's data is completely separate
- **Efficient Calculations**: Daily totals calculated with optimized queries
- **Goal Validation**: Server-side validation for all nutrition values
- **Rate Limiting**: Recommended for production use

---

## 🚀 Production Considerations

1. **Database Indexing**: Add indexes on user_id and created_at fields
2. **Caching**: Cache daily summaries for better performance
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Backup Strategy**: Regular database backups
5. **Monitoring**: Log API usage and performance metrics

This enhanced API provides a complete nutrition tracking system with goal management and progress monitoring!