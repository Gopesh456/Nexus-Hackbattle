export interface User {
  id: string;
  user: string;
  email?: string;
}

export interface RegisterResponse {
  message?: string;
  user_id?: number;
  tokens?: string | { access: string; refresh: string };
}

export interface LoginResponse {
  message: string;
  user: {
    id: number;
    username: string;
    email?: string;
  };
  tokens: {
    access: string;
    refresh: string;
  };
}

export interface AuthContextType {
  user: User | null;
  login: (user: string, password: string) => Promise<void>;
  register: (user: string, password: string) => Promise<RegisterResponse>;
  logout: () => void;
  isLoading: boolean;
}

export interface HealthProfile {
  height_cm: number;
  weight_kg: number;
  activity_level: "sedentary" | "light" | "moderate" | "active" | "very-active";
  chronic_conditions: string[];
  allergies: string[];
  current_medications: string[];
  blood_group: string;
  daily_calorie_goal: number;
  daily_protein_goal: number;
  emergency_contact: {
    name: string;
    relationship: string;
    phone: string;
  };
}

export interface BasicInfo {
  full_name: string;
  date_of_birth: string;
  gender: string;
  location: string;
  email: string;
  phone: string;
}

export interface FoodEntry {
  id: string;
  name: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  timestamp: Date;
  meal: "breakfast" | "lunch" | "dinner" | "snack";
}

export interface FoodLog {
  id: string;
  food_name: string;
  quantity: number;
  unit: string;
  time: string;
  meal_type: "breakfast" | "lunch" | "dinner" | "snack";
  nutrition: NutritionDetails;
  created_at: string;
}

export interface NutritionDetails {
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber?: number;
  sugar?: number;
  sodium?: number;
  cholesterol?: number;
  vitamin_a?: number;
  vitamin_c?: number;
  calcium?: number;
  iron?: number;
}

export interface RealtimeHealthData {
  heart_rate: number;
  steps: number;
  calories_burned: number;
  blood_pressure?: {
    systolic: number;
    diastolic: number;
  };
  blood_oxygen?: number;
  stress_level?: number;
  temperature?: number;
  timestamp: string;
}

export interface DailyNutritionSummary {
  total_calories: number;
  total_protein: number;
  total_carbs: number;
  total_fat: number;
  goal_calories: number;
  goal_protein: number;
  goal_carbs: number;
  goal_fat: number;
  meals: {
    breakfast: { calories: number; items: number };
    lunch: { calories: number; items: number };
    dinner: { calories: number; items: number };
    snack: { calories: number; items: number };
  };
}

export interface HealthMetrics {
  weight: number;
  steps: number;
  waterIntake: number;
  sleep: number;
  heartRate: number;
  caloriesBurned: number;
}
