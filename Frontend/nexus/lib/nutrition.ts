export interface NutritionRequest {
  token: string
  food_name: string
  quantity: number
  unit: string
}

export interface NutritionResponse {
  food_name: string
  quantity: number
  unit: string
  quantity_in_grams: number
  nutrition_per_100g: {
    calories: number
    protein: number
    fat: number
    carbohydrates: number
    fiber: number
    sugar: number
  }
  total_nutrition: {
    calories: number
    protein: number
    carbohydrates: number
    fat: number
    fiber: number
    sugar: number
  }
  usda_food_name: string
  stored_id: number
}

export interface NutritionGoals {
  id: number
  username: string
  daily_calories_goal: number
  daily_protein_goal: number
  daily_carbs_goal: number
  daily_fat_goal: number
  daily_fiber_goal: number
  daily_sugar_goal: number
  created_at: string
}

export interface NutritionHistory {
  user: string
  count: number
  results: Array<{
    id: number
    username: string
    food_name: string
    quantity: number
    usda_food_id: string
    calories_per_100g: number
    protein_per_100g: number
    carbs_per_100g: number
    fat_per_100g: number
    fiber_per_100g: number
    sugar_per_100g: number
    total_calories: number
    total_protein: number
    total_carbs: number
    total_fat: number
    total_fiber: number
    total_sugar: number
    created_at: string
    user: number
  }>
}

export interface NutritionSummary {
  user: string
  summary: {
    date: string
    consumed: {
      calories: number
      protein: number
      carbohydrates: number
      fat: number
      fiber: number
      sugar: number
    }
    goals: {
      calories: number
      protein: number
      carbohydrates: number
      fat: number
      fiber: number
      sugar: number
    }
    progress: {
      calories_percentage: number
      calories_remaining: number
      protein_percentage: number
      protein_remaining: number
      carbohydrates_percentage: number
      carbohydrates_remaining: number
      fat_percentage: number
      fat_remaining: number
      fiber_percentage: number
      fiber_remaining: number
      sugar_percentage: number
      sugar_remaining: number
    }
    entries_count: number
  }
}

export const logNutrition = async (data: NutritionRequest, baseUrl: string): Promise<NutritionResponse> => {
  const response = await fetch(`${baseUrl}/nutrition`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error("Failed to log nutrition")
  }

  return response.json()
}

export const getNutritionGoals = async (token: string, baseUrl: string): Promise<NutritionGoals> => {
  const response = await fetch(`${baseUrl}/goal`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ token }),
  })

  if (!response.ok) {
    throw new Error("Failed to get nutrition goals")
  }

  return response.json()
}

export const getNutritionHistory = async (token: string, baseUrl: string): Promise<NutritionHistory> => {
  const response = await fetch(`${baseUrl}/nutrition/history`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ token }),
  })

  if (!response.ok) {
    throw new Error("Failed to get nutrition history")
  }

  return response.json()
}

export const getNutritionSummary = async (token: string, baseUrl: string): Promise<NutritionSummary> => {
  const response = await fetch(`${baseUrl}/summary`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ token }),
  })

  if (!response.ok) {
    throw new Error("Failed to get nutrition summary")
  }

  return response.json()
}

export { getAuthToken } from "./auth"
