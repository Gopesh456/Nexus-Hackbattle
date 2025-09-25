// Test file to validate nutrition API integration
// This file can be deleted after testing

import { apiClient } from "./utils/api";

export const testNutritionIntegration = async () => {
  console.log("Testing Nutrition API Integration...");

  try {
    // Test 1: Get nutrition goals
    console.log("1. Testing getNutritionGoals...");
    const goals = await apiClient.getNutritionGoals();
    console.log("Nutrition Goals:", goals);

    // Test 2: Add food entry with unit conversion
    console.log("2. Testing addFoodEntry with unit conversion...");
    const foodEntry = await apiClient.addFoodEntry(
      "Apple",
      1, // quantity
      "kg" // unit (should be converted to grams)
    );
    console.log("Food Entry Response:", foodEntry);

    // Test 3: Get nutrition history
    console.log("3. Testing getNutritionHistory...");
    const history = await apiClient.getNutritionHistory();
    console.log("Nutrition History:", history);

    // Test 4: Get daily summary
    console.log("4. Testing getDailySummary...");
    const summary = await apiClient.getDailySummary();
    console.log("Daily Summary:", summary);

    console.log("All tests completed successfully!");
  } catch (error) {
    console.error("Nutrition API Integration Test Failed:", error);
  }
};

// Example unit conversions for reference:
export const unitConversions = {
  // Weight conversions to grams
  kg: (value: number) => value * 1000,
  lb: (value: number) => value * 453.592,
  oz: (value: number) => value * 28.3495,
  lbs: (value: number) => value * 453.592,
  pound: (value: number) => value * 453.592,
  pounds: (value: number) => value * 453.592,
  ounce: (value: number) => value * 28.3495,
  ounces: (value: number) => value * 28.3495,

  // Volume conversions to grams (approximate for water-like density)
  ml: (value: number) => value, // 1ml ≈ 1g for water
  l: (value: number) => value * 1000,
  liter: (value: number) => value * 1000,
  liters: (value: number) => value * 1000,
  cup: (value: number) => value * 240, // 1 cup ≈ 240ml
  cups: (value: number) => value * 240,
  tbsp: (value: number) => value * 15, // 1 tbsp ≈ 15ml
  tsp: (value: number) => value * 5, // 1 tsp ≈ 5ml

  // Default case
  g: (value: number) => value,
  gram: (value: number) => value,
  grams: (value: number) => value,
};
