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

export interface HealthMetrics {
  weight: number;
  steps: number;
  waterIntake: number;
  sleep: number;
  heartRate: number;
  caloriesBurned: number;
}
