# Food Nutrition API with JWT Authentication

## Overview
This API provides endpoints to manage user-specific nutritional information using JWT authentication. Users must authenticate to store and retrieve their personal food diary data.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
All nutrition endpoints require JWT authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### 1. User Registration
**POST** `/register/`

Register a new user account.

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securePassword123"
}
```

**Success Response (201):**
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

### 2. User Login
**POST** `/login/`

Authenticate user and get JWT tokens.

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "securePassword123"
}
```

**Success Response (200):**
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

### 3. Add Food Entry (Protected)
**POST** `/nutrition/`

Add a new food entry to the user's diary and get nutritional information.

**Headers:**
```
Authorization: Bearer <jwt_access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "food_name": "apple",
    "quantity": 150
}
```

**Success Response (200):**
```json
{
    "food_name": "apple",
    "quantity": 150,
    "unit": "grams",
    "nutrition_per_100g": {
        "calories": 52.0,
        "protein": 0.26,
        "carbohydrates": 13.81,
        "fat": 0.17,
        "fiber": 2.4,
        "sugar": 10.39
    },
    "total_nutrition": {
        "calories": 78.0,
        "protein": 0.39,
        "carbohydrates": 20.72,
        "fat": 0.26,
        "fiber": 3.6,
        "sugar": 15.59
    },
    "usda_food_name": "Apples, raw, with skin",
    "stored_id": 1
}
```

### 4. Get User's Food History (Protected)
**GET** `/nutrition/history/`

Retrieve the authenticated user's food diary history.

**Headers:**
```
Authorization: Bearer <jwt_access_token>
```

**Success Response (200):**
```json
{
    "user": "john_doe",
    "count": 5,
    "results": [
        {
            "id": 1,
            "username": "john_doe",
            "food_name": "apple",
            "quantity": 150.0,
            "usda_food_id": "171688",
            "calories_per_100g": 52.0,
            "protein_per_100g": 0.26,
            "carbs_per_100g": 13.81,
            "fat_per_100g": 0.17,
            "fiber_per_100g": 2.4,
            "sugar_per_100g": 10.39,
            "total_calories": 78.0,
            "total_protein": 0.39,
            "total_carbs": 20.72,
            "total_fat": 0.26,
            "total_fiber": 3.6,
            "total_sugar": 15.59,
            "created_at": "2025-09-24T22:30:00Z"
        }
    ]
}
```

### 5. Token Refresh
**POST** `/token/refresh/`

Refresh access token using refresh token.

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Frontend Integration Examples

### JavaScript Authentication Flow
```javascript
class FoodNutritionAPI {
    constructor() {
        this.baseURL = 'http://127.0.0.1:8000/api';
        this.accessToken = localStorage.getItem('access_token');
    }

    // User Registration
    async register(username, email, password) {
        const response = await fetch(`${this.baseURL}/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            this.accessToken = data.tokens.access;
            localStorage.setItem('access_token', data.tokens.access);
            localStorage.setItem('refresh_token', data.tokens.refresh);
            return data;
        }
        throw new Error('Registration failed');
    }

    // User Login
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
            localStorage.setItem('refresh_token', data.tokens.refresh);
            return data;
        }
        throw new Error('Login failed');
    }

    // Add Food Entry
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

        if (response.ok) {
            return await response.json();
        } else if (response.status === 401) {
            // Token expired, try to refresh
            await this.refreshToken();
            return this.addFoodEntry(foodName, quantity);
        }
        throw new Error('Failed to add food entry');
    }

    // Get Food History
    async getFoodHistory() {
        const response = await fetch(`${this.baseURL}/nutrition/history/`, {
            headers: {
                'Authorization': `Bearer ${this.accessToken}`
            }
        });

        if (response.ok) {
            return await response.json();
        } else if (response.status === 401) {
            await this.refreshToken();
            return this.getFoodHistory();
        }
        throw new Error('Failed to get food history');
    }

    // Refresh Token
    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await fetch(`${this.baseURL}/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            this.accessToken = data.access;
            localStorage.setItem('access_token', data.access);
        } else {
            // Refresh token invalid, redirect to login
            this.logout();
            throw new Error('Session expired');
        }
    }

    // Logout
    logout() {
        this.accessToken = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }
}

// Usage Example
const api = new FoodNutritionAPI();

// Register/Login first
await api.login('john_doe', 'password123');

// Add food entries
const result = await api.addFoodEntry('banana', 120);
console.log('Added food:', result);

// Get history
const history = await api.getFoodHistory();
console.log('Food history:', history);
```

### React Component Example
```jsx
import React, { useState, useEffect } from 'react';

function FoodDiary() {
    const [accessToken, setAccessToken] = useState(localStorage.getItem('access_token'));
    const [foodHistory, setFoodHistory] = useState([]);
    const [foodName, setFoodName] = useState('');
    const [quantity, setQuantity] = useState('');

    useEffect(() => {
        if (accessToken) {
            fetchFoodHistory();
        }
    }, [accessToken]);

    const fetchFoodHistory = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/nutrition/history/', {
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setFoodHistory(data.results);
            }
        } catch (error) {
            console.error('Failed to fetch food history:', error);
        }
    };

    const addFoodEntry = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:8000/api/nutrition/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    food_name: foodName,
                    quantity: parseFloat(quantity)
                })
            });

            if (response.ok) {
                const newEntry = await response.json();
                setFoodHistory([newEntry, ...foodHistory]);
                setFoodName('');
                setQuantity('');
            }
        } catch (error) {
            console.error('Failed to add food entry:', error);
        }
    };

    if (!accessToken) {
        return <div>Please login to access your food diary</div>;
    }

    return (
        <div>
            <h2>My Food Diary</h2>
            
            <form onSubmit={addFoodEntry}>
                <input
                    type="text"
                    placeholder="Food name"
                    value={foodName}
                    onChange={(e) => setFoodName(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Quantity (grams)"
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                    required
                />
                <button type="submit">Add Food</button>
            </form>

            <h3>Food History</h3>
            {foodHistory.map(entry => (
                <div key={entry.id}>
                    <h4>{entry.food_name} ({entry.quantity}g)</h4>
                    <p>Calories: {entry.total_calories}</p>
                    <p>Protein: {entry.total_protein}g</p>
                    <p>Date: {new Date(entry.created_at).toLocaleDateString()}</p>
                </div>
            ))}
        </div>
    );
}
```

## Error Responses

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```
or
```json
{
    "detail": "Given token not valid for any token type"
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **User Isolation**: Each user can only access their own food data
3. **Token Expiry**: Access tokens expire in 60 minutes
4. **Token Refresh**: Refresh tokens valid for 7 days
5. **CORS Protection**: Configured for specific frontend domains

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create `.env` file with:
   ```
   USDA_API_KEY=your_usda_api_key_here
   SECRET_KEY=your_django_secret_key
   ```

3. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Server**
   ```bash
   python manage.py runserver
   ```

## Testing with cURL

### Register User
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Add Food Entry (with token)
```bash
curl -X POST http://127.0.0.1:8000/api/nutrition/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"food_name":"apple","quantity":150}'
```

### Get Food History (with token)
```bash
curl -X GET http://127.0.0.1:8000/api/nutrition/history/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```