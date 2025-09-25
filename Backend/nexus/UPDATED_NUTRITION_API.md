# Updated Nutrition API Documentation

## Overview
The nutrition endpoint has been updated to accept additional fields for meal tracking: `time` and `meal_type`.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Endpoint
**POST** `/nutrition/`

Get nutrition information for a food item from USDA API and store it with meal tracking data.

## New Request Format

### Required Fields
- `token`: JWT authentication token
- `food_name`: Name of the food item
- `quantity`: Amount of food
- `unit`: Unit of measurement

### Optional New Fields
- `time`: Time when food was consumed (HH:MM format)
- `meal_type`: Type of meal (breakfast, lunch, dinner, snack)

### Complete Request Format
```json
{
  "token": "your_jwt_token_here",
  "food_name": "Apple",
  "quantity": 100,
  "unit": "g", 
  "time": "08:30",
  "meal_type": "breakfast"
}
```

## Field Details

### **time** (Optional)
- **Format**: HH:MM (24-hour format)
- **Examples**: "08:30", "12:45", "19:15"
- **Description**: Time when the food was consumed
- **Default**: `null` if not provided

### **meal_type** (Optional)
- **Allowed Values**: 
  - `"breakfast"` - Morning meal
  - `"lunch"` - Midday meal  
  - `"dinner"` - Evening meal
  - `"snack"` - Snack between meals
- **Default**: `null` if not provided

### **unit** (Required)
- **Allowed Values**: `"g"`, `"kg"`, `"oz"`, `"lb"`, `"cup"`, `"ml"`, `"l"`
- **Default**: `"g"`

## Example Requests

### 1. Complete Request with All Fields
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "food_name": "Apple",
  "quantity": 100,
  "unit": "g", 
  "time": "08:30",
  "meal_type": "breakfast"
}
```

### 2. Lunch Example
```json
{
  "token": "your_jwt_token_here",
  "food_name": "Banana",
  "quantity": 150,
  "unit": "g", 
  "time": "12:45",
  "meal_type": "lunch"
}
```

### 3. Evening Snack Example
```json
{
  "token": "your_jwt_token_here",
  "food_name": "Almonds",
  "quantity": 30,
  "unit": "g", 
  "time": "19:15",
  "meal_type": "snack"
}
```

### 4. Without Time/Meal Type (Backward Compatible)
```json
{
  "token": "your_jwt_token_here",
  "food_name": "Orange",
  "quantity": 80,
  "unit": "g"
}
```

## Response Format

The response now includes the time and meal_type fields:

```json
{
  "food_name": "Apple",
  "quantity": 100.0,
  "unit": "g",
  "time": "08:30",
  "meal_type": "breakfast",
  "quantity_in_grams": 100.0,
  "nutrition_per_100g": {
    "calories": 52.0,
    "protein": 0.26,
    "carbohydrates": 13.81,
    "fat": 0.17,
    "fiber": 2.4,
    "sugar": 10.39
  },
  "total_nutrition": {
    "calories": 52.0,
    "protein": 0.26,
    "carbohydrates": 13.81,
    "fat": 0.17,
    "fiber": 2.4,
    "sugar": 10.39
  },
  "usda_food_name": "Apples, raw, with skin",
  "stored_id": 1
}
```

## Database Changes

### FoodNutrition Model Updates
Two new fields have been added to the FoodNutrition model:

```python
time = models.TimeField(null=True, blank=True, help_text="Time when food was consumed (HH:MM format)")
meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, null=True, blank=True, help_text="Type of meal")
```

### Meal Type Choices
```python
MEAL_TYPE_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('snack', 'Snack')
]
```

## curl Examples

### Complete Request
```bash
curl -X POST http://127.0.0.1:8000/api/nutrition/ \
-H "Content-Type: application/json" \
-d '{
  "token": "your_jwt_token_here",
  "food_name": "Apple",
  "quantity": 100,
  "unit": "g", 
  "time": "08:30",
  "meal_type": "breakfast"
}'
```

### Lunch Example
```bash
curl -X POST http://127.0.0.1:8000/api/nutrition/ \
-H "Content-Type: application/json" \
-d '{
  "token": "your_jwt_token_here",
  "food_name": "Chicken Breast",
  "quantity": 200,
  "unit": "g", 
  "time": "13:00",
  "meal_type": "lunch"
}'
```

### Snack Example
```bash
curl -X POST http://127.0.0.1:8000/api/nutrition/ \
-H "Content-Type: application/json" \
-d '{
  "token": "your_jwt_token_here",
  "food_name": "Greek Yogurt",
  "quantity": 150,
  "unit": "g", 
  "time": "15:30",
  "meal_type": "snack"
}'
```

## Backward Compatibility

✅ **The API remains fully backward compatible**

- Existing requests without `time` and `meal_type` will continue to work
- Optional fields default to `null` when not provided
- All existing functionality is preserved

## Error Handling

### Invalid Time Format
```json
{
  "time": ["Enter a valid time."]
}
```

### Invalid Meal Type
```json
{
  "meal_type": ["Select a valid choice. invalid_meal is not one of the available choices."]
}
```

### Missing Required Fields
```json
{
  "food_name": ["This field is required."],
  "quantity": ["This field is required."]
}
```

## Benefits of the Update

1. **Meal Tracking**: Users can now track when they eat specific foods
2. **Meal Type Classification**: Foods can be categorized by meal type
3. **Better Analytics**: Time-based nutrition analysis becomes possible
4. **Enhanced User Experience**: More detailed food logging capabilities
5. **Backward Compatible**: No breaking changes for existing clients

## Migration Applied
- Migration `0016_foodnutrition_meal_type_foodnutrition_time.py` has been successfully applied
- Database schema updated to include the new fields
- All existing data remains intact