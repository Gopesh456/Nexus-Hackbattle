# Nutrition API Integration Summary

## Overview

Updated the nutrition system to integrate with new API endpoints that require JWT tokens in request bodies and handle unit conversion to grams.

## API Endpoints Updated

### 1. Nutrition Goals Endpoint (`nutrition/goals/`)

- **Method**: POST
- **Authentication**: JWT token in request body
- **Purpose**: Get user's nutrition goals (calories, protein, carbs, fat)
- **Response Format**:
  ```json
  {
    "calories": 2200,
    "protein": 110,
    "carbs": 275,
    "fat": 73
  }
  ```

### 2. Nutrition Entry Endpoint (`nutrition/`)

- **Method**: POST
- **Authentication**: JWT token in request body
- **Purpose**: Add food entries and get nutrition history
- **Request Format**:
  ```json
  {
    "food_name": "Apple",
    "quantity": 1000, // Always in grams
    "token": "jwt_token_here"
  }
  ```
- **Response Format**:
  ```json
  {
    "total_nutrition": {
      "calories": 520,
      "protein": 1.04,
      "carbohydrates": 138.28,
      "fat": 0.34,
      "fiber": 12.4,
      "sugar": 103.9
    },
    "results": [
      {
        "id": 1,
        "food_name": "Apple",
        "quantity": 1000,
        "nutrition": {...},
        "created_at": "2024-01-15T10:30:00Z"
      }
    ]
  }
  ```

## Key Changes Made

### 1. API Client Updates (`src/utils/api.ts`)

#### Unit Conversion System

- Added automatic conversion from various units to grams
- Supported units: kg, lb, oz, cup, tbsp, tsp, ml, l
- Conversions are applied in `addFoodEntry` method before sending to API

```typescript
// Example conversions:
kg → grams: quantity * 1000
lb → grams: quantity * 453.592
oz → grams: quantity * 28.3495
cup → grams: quantity * 240 (liquid approx)
```

#### Updated Methods:

- `addFoodEntry()`: Now converts units to grams and includes JWT token in body
- `getNutritionGoals()`: New method for fetching nutrition goals using JWT token
- `setNutritionGoals()`: Updated to use new endpoint format
- `updateNutritionGoals()`: Updated to use new endpoint format
- `getDailySummary()`: Updated to combine nutrition goals and consumed nutrition data

### 2. FoodDiary Component Updates (`src/components/dashboard/FoodDiary.tsx`)

#### API Response Handling

- Updated `fetchNutritionData()` to handle new response format with `total_nutrition` object
- Updated `loadFoodLogs()` to map `results` array to `FoodLog` interface
- Fixed field mapping: `carbohydrates` → `carbs` in API response

#### Data Transformation

```typescript
// Old format: Direct nutrition values
// New format: total_nutrition object + results array
const nutritionData: NutritionDetails = {
  calories: data.total_nutrition?.calories || 0,
  protein: data.total_nutrition?.protein || 0,
  carbs: data.total_nutrition?.carbohydrates || 0, // Note: carbohydrates in API
  fat: data.total_nutrition?.fat || 0,
  // ... other fields
};
```

### 3. DailyNutritionSummary Component Updates

#### Combined Data Fetching

- Updated `getDailySummary()` to fetch both nutrition goals and consumed nutrition
- Combines data from `getNutritionGoals()` and `getNutritionHistory()` APIs
- Provides fallback values for goals and consumed nutrition

## Unit Conversion Reference

| Unit | Conversion to Grams | Example      |
| ---- | ------------------- | ------------ |
| kg   | × 1000              | 1 kg → 1000g |
| lb   | × 453.592           | 1 lb → 454g  |
| oz   | × 28.3495           | 1 oz → 28g   |
| cup  | × 240               | 1 cup → 240g |
| tbsp | × 15                | 1 tbsp → 15g |
| tsp  | × 5                 | 1 tsp → 5g   |
| ml   | × 1                 | 1 ml → 1g    |
| l    | × 1000              | 1 l → 1000g  |

## Usage Examples

### Adding Food Entry with Unit Conversion

```typescript
// User enters: 2 cups of rice
await apiClient.addFoodEntry("Rice", 2, "cup");
// API receives: { food_name: "Rice", quantity: 480, token: "..." }
```

### Fetching Nutrition Goals

```typescript
const goals = await apiClient.getNutritionGoals();
// Returns: { calories: 2200, protein: 110, carbs: 275, fat: 73 }
```

### Getting Daily Summary

```typescript
const summary = await apiClient.getDailySummary();
// Combines goals + consumed nutrition into DailyNutritionSummary format
```

## Testing

A test file has been created at `src/test_nutrition_integration.ts` to validate:

1. Nutrition goals fetching
2. Food entry with unit conversion
3. Nutrition history retrieval
4. Daily summary generation

## Backend Integration Notes

- Ensure JWT tokens are properly validated in the backend endpoints
- Backend should expect quantities in grams for the `nutrition/` endpoint
- Response format should match the documented structure with `total_nutrition` and `results` fields
- The `nutrition/goals/` endpoint should accept JWT token in the request body and return the user's nutrition goals

## Next Steps

1. Test the integration with the actual backend API
2. Verify unit conversion accuracy with nutritional data
3. Add error handling for invalid units or conversion failures
4. Consider adding more unit types if needed (e.g., servings, pieces)
5. Implement caching for nutrition goals to reduce API calls
