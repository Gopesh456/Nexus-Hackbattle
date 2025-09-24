# Food Nutrition API Documentation

## Overview
This API provides endpoints to get nutritional information for food items using the USDA FoodData Central API. It receives food name and quantity from the frontend, fetches nutrition data, and stores it in the database.

## Base URL
```
http://127.0.0.1:8000/api
```

## Endpoints

### 1. Get Food Nutrition Data
**POST** `/nutrition/`

Retrieves nutritional information for a food item and stores it in the database.

#### Request Body
```json
{
    "food_name": "apple",
    "quantity": 150
}
```

- `food_name` (string, required): Name of the food item
- `quantity` (number, required): Quantity in grams (minimum: 0.1)

#### Success Response (200)
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
    "usda_food_name": "Apples, raw, with skin (Includes foods for USDA's Food Distribution Program)",
    "stored_id": 1
}
```

#### Error Responses
- **400 Bad Request**: Invalid input data
- **404 Not Found**: No nutrition data found for the food item
- **503 Service Unavailable**: USDA API is unavailable
- **500 Internal Server Error**: Server error

### 2. Get Nutrition History
**GET** `/nutrition/history/`

Retrieves the history of stored nutrition data (latest 50 records).

#### Success Response (200)
```json
{
    "count": 25,
    "results": [
        {
            "id": 1,
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
            "created_at": "2024-01-01T10:30:00Z"
        }
    ]
}
```

## Frontend Integration Examples

### JavaScript (Fetch API)
```javascript
// Get nutrition data
async function getNutritionData(foodName, quantity) {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/nutrition/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                food_name: foodName,
                quantity: quantity
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('Nutrition data:', data);
            return data;
        } else {
            const error = await response.json();
            console.error('Error:', error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

// Usage
getNutritionData('banana', 120);
```

### React Component Example
```jsx
import React, { useState } from 'react';

function FoodNutritionForm() {
    const [foodName, setFoodName] = useState('');
    const [quantity, setQuantity] = useState('');
    const [nutritionData, setNutritionData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await fetch('http://127.0.0.1:8000/api/nutrition/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    food_name: foodName,
                    quantity: parseFloat(quantity)
                })
            });

            if (response.ok) {
                const data = await response.json();
                setNutritionData(data);
            } else {
                const errorData = await response.json();
                setError(errorData.error || 'Failed to get nutrition data');
            }
        } catch (error) {
            setError('Network error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Food name (e.g., apple)"
                    value={foodName}
                    onChange={(e) => setFoodName(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Quantity in grams"
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                    min="0.1"
                    step="0.1"
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Getting nutrition data...' : 'Get Nutrition Info'}
                </button>
            </form>

            {error && <div className="error">{error}</div>}

            {nutritionData && (
                <div className="nutrition-results">
                    <h3>{nutritionData.food_name} ({nutritionData.quantity}g)</h3>
                    <div className="nutrition-grid">
                        <div>Calories: {nutritionData.total_nutrition.calories}</div>
                        <div>Protein: {nutritionData.total_nutrition.protein}g</div>
                        <div>Carbs: {nutritionData.total_nutrition.carbohydrates}g</div>
                        <div>Fat: {nutritionData.total_nutrition.fat}g</div>
                        <div>Fiber: {nutritionData.total_nutrition.fiber}g</div>
                        <div>Sugar: {nutritionData.total_nutrition.sugar}g</div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default FoodNutritionForm;
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the Django project root:
   ```
   USDA_API_KEY=your_usda_api_key_here
   SECRET_KEY=your_django_secret_key
   ```

3. **Get USDA API Key**
   - Visit: https://fdc.nal.usda.gov/api-guide.html
   - Sign up for a free API key
   - Add it to your `.env` file

4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start Server**
   ```bash
   python manage.py runserver
   ```

## Database Schema

The `FoodNutrition` model stores:
- Food name and quantity
- USDA food ID for reference
- Nutrition values per 100g
- Calculated total nutrition for the specified quantity
- Timestamp of when the data was stored

## Notes

- All nutrition values are automatically calculated and stored
- The API handles unit conversion (USDA data is per 100g)
- CORS is configured for localhost:3000 (React/Next.js default)
- No authentication required for these endpoints
- Data is stored for future reference and analytics