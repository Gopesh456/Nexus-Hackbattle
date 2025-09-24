export interface LoginCredentials {
  user: string
  password: string
}

export interface AuthResponse {
  token: string
}

export interface BasicInfo {
  token: string
  full_name: string
  date_of_birth: string
  gender: string
  location: string
  email: string
  phone: string
}

export interface HealthProfile {
  token: string
  height_cm: number
  weight_kg: number
  chronic_conditions: string[]
  allergies: string[]
  current_medications: string[]
  blood_group: string
  daily_calorie_goal: number
  daily_protein_goal: number
  daily_carbs_goal: number
  daily_fat_goal: number
  daily_fiber_goal: number
  daily_sugar_goal: number
  emergency_contact: {
    name: string
    relationship: string
    phone: string
  }
}

// Cookie management
export const setAuthToken = (token: string) => {
  document.cookie = `auth_token=${token}; path=/; max-age=${7 * 24 * 60 * 60}; secure; samesite=strict`
}

export const getAuthToken = (): string | null => {
  if (typeof document === "undefined") return null
  const cookies = document.cookie.split(";")
  const authCookie = cookies.find((cookie) => cookie.trim().startsWith("auth_token="))
  return authCookie ? authCookie.split("=")[1] : null
}

export const removeAuthToken = () => {
  document.cookie = "auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"
}

// API calls
export const login = async (credentials: LoginCredentials, baseUrl: string): Promise<AuthResponse> => {
  const response = await fetch(`${baseUrl}/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  })

  if (!response.ok) {
    throw new Error("Login failed")
  }

  return response.json()
}

export const register = async (credentials: LoginCredentials, baseUrl: string): Promise<AuthResponse> => {
  const response = await fetch(`${baseUrl}/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  })

  if (!response.ok) {
    throw new Error("Registration failed")
  }

  return response.json()
}

export const storeBasicInfo = async (data: BasicInfo, baseUrl: string) => {
  const response = await fetch(`${baseUrl}/basic-info/store/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error("Failed to store basic info")
  }

  return response.json()
}

export const storeHealthProfile = async (data: HealthProfile, baseUrl: string) => {
  const response = await fetch(`${baseUrl}/health-profile/store/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error("Failed to store health profile")
  }

  return response.json()
}
