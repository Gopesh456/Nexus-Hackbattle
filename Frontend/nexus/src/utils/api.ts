import Cookies from "js-cookie";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

class ApiClient {
  private getAuthHeaders(): Record<string, string> {
    const token = Cookies.get("token");
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  async post(endpoint: string, data: Record<string, unknown>) {
    const url = `${API_BASE}/${endpoint}`;

    try {
      const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          ...this.getAuthHeaders(),
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        // Handle Django field validation errors
        if (errorData.username && Array.isArray(errorData.username)) {
          throw new Error(errorData.username[0]); // "A user with that username already exists."
        }

        if (errorData.password && Array.isArray(errorData.password)) {
          throw new Error(errorData.password[0]);
        }

        if (errorData.email && Array.isArray(errorData.email)) {
          throw new Error(errorData.email[0]);
        }

        // Handle non_field_errors (general validation errors)
        if (
          errorData.non_field_errors &&
          Array.isArray(errorData.non_field_errors)
        ) {
          throw new Error(errorData.non_field_errors[0]);
        }

        // Handle general error messages
        throw new Error(
          errorData.message ||
            errorData.error ||
            errorData.detail ||
            `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error("Network error occurred");
    }
  }

  async storeBasicInfo(data: Record<string, unknown>) {
    return this.post("basic-info/store/", data);
  }

  async storeHealthProfile(data: Record<string, unknown>) {
    return this.post("health-profile/store/", data);
  }

  async getData(endpoint: string, data: Record<string, unknown> = {}) {
    // Use POST method for data retrieval as well
    return this.post(endpoint, data);
  }

  // Authentication endpoints
  async register(username: string, password: string) {
    const response = await this.post("register/", { username, password });

    // Store JWT token in cookie if registration is successful
    if (response.tokens) {
      Cookies.set("token", response.tokens, { expires: 7 }); // Store for 7 days
    }

    return response;
  }

  async login(username: string, password: string) {
    const response = await this.post("login/", { username, password });

    // Store JWT token in cookie if login is successful
    if (response.tokens) {
      Cookies.set("token", response.tokens, { expires: 7 }); // Store for 7 days
    }

    return response;
  }

  async logout() {
    // Remove token from cookies
    Cookies.remove("token");
    return Promise.resolve({ message: "Logged out successfully" });
  }

  // Food Nutrition POST endpoints
  async addFoodEntry(
    foodName: string,
    quantity: number,
    unit: string = "g",
    mealType: string = "breakfast",
    time: string = new Date().toTimeString().slice(0, 5)
  ) {
    const token = Cookies.get("token");

    // Convert quantity to grams if not already in grams
    let quantityInGrams = quantity;
    const unitLower = unit.toLowerCase();

    // Common unit conversions to grams
    switch (unitLower) {
      case "kg":
      case "kilogram":
      case "kilograms":
        quantityInGrams = quantity * 1000;
        break;
      case "lb":
      case "pound":
      case "pounds":
        quantityInGrams = quantity * 453.592;
        break;
      case "oz":
      case "ounce":
      case "ounces":
        quantityInGrams = quantity * 28.3495;
        break;
      case "cup":
      case "cups":
        quantityInGrams = quantity * 240; // Approximate for liquid
        break;
      case "tbsp":
      case "tablespoon":
      case "tablespoons":
        quantityInGrams = quantity * 15;
        break;
      case "tsp":
      case "teaspoon":
      case "teaspoons":
        quantityInGrams = quantity * 5;
        break;
      case "g":
      case "gram":
      case "grams":
      default:
        quantityInGrams = quantity;
        break;
    }

    return this.post("nutrition/", {
      food_name: foodName,
      quantity: Math.round(quantityInGrams), // Ensure integer grams
      meal_type: mealType,
      time: time,
      token: token,
    });
  }

  async getNutritionHistory() {
    const token = Cookies.get("token");
    return this.post("nutrition/", { token });
  }

  async searchFoodUSDA(query: string) {
    return this.post("nutrition/search/", {
      query: query,
    });
  }

  // Get nutrition info without saving (for preview)
  async getNutritionInfo(
    foodName: string,
    quantity: number,
    unit: string = "g"
  ) {
    const token = Cookies.get("token");

    // Convert quantity to grams if not already in grams
    let quantityInGrams = quantity;
    const unitLower = unit.toLowerCase();

    // Common unit conversions to grams
    switch (unitLower) {
      case "kg":
      case "kilogram":
      case "kilograms":
        quantityInGrams = quantity * 1000;
        break;
      case "lb":
      case "pound":
      case "pounds":
        quantityInGrams = quantity * 453.592;
        break;
      case "oz":
      case "ounce":
      case "ounces":
        quantityInGrams = quantity * 28.3495;
        break;
      case "cup":
      case "cups":
        quantityInGrams = quantity * 240;
        break;
      case "tbsp":
      case "tablespoon":
      case "tablespoons":
        quantityInGrams = quantity * 15;
        break;
      case "tsp":
      case "teaspoon":
      case "teaspoons":
        quantityInGrams = quantity * 5;
        break;
      case "g":
      case "gram":
      case "grams":
      default:
        quantityInGrams = quantity;
        break;
    }

    return this.post("nutrition/preview/", {
      food_name: foodName,
      quantity: Math.round(quantityInGrams),
      token: token,
    });
  }

  async deleteNutritionEntry(entryId: number) {
    return this.post("nutrition/delete/", {
      id: entryId,
    });
  }

  async editNutritionEntry(
    entryId: number,
    foodName: string,
    quantity: number,
    unit: string,
    time: string,
    mealType: string
  ) {
    return this.post("nutrition/edit/", {
      id: entryId,
      food_name: foodName,
      quantity: quantity,
      unit: unit,
      time: time,
      meal_type: mealType,
    });
  }

  // Dashboard specific endpoints
  async getDailySummary() {
    try {
      // Get nutrition goals
      const goalsResponse = await this.getNutritionGoals();

      // Get today's consumed nutrition
      const nutritionResponse = await this.getNutritionHistory();

      // Combine the data
      return {
        data: {
          goal_calories: goalsResponse.calories || 2200,
          goal_protein: goalsResponse.protein || 110,
          goal_carbs: goalsResponse.carbs || 275,
          goal_fat: goalsResponse.fat || 73,
          total_calories: nutritionResponse.total_nutrition?.calories || 0,
          total_protein: nutritionResponse.total_nutrition?.protein || 0,
          total_carbs: nutritionResponse.total_nutrition?.carbs || 0,
          total_fat: nutritionResponse.total_nutrition?.fat || 0,
          meals: {
            breakfast: { calories: 0, items: 0 },
            lunch: { calories: 0, items: 0 },
            dinner: { calories: 0, items: 0 },
            snack: { calories: 0, items: 0 },
          },
        },
      };
    } catch (error) {
      console.error("Error fetching daily summary:", error);
      throw error;
    }
  }

  async getRealtimeHealthData() {
    return this.post("health/realtime/", {});
  }

  // SmartWatch WebSocket connection info (for reference)
  // The SmartWatchMetrics component connects directly to:
  // wss://jarrod-senescent-beatris.ngrok-free.dev

  // User Goals POST endpoints
  async setNutritionGoals(goals: Record<string, unknown>) {
    const token = Cookies.get("token");
    return this.post("nutrition/goals/", { ...goals, token });
  }

  async getNutritionGoals() {
    const token = Cookies.get("token");
    return this.post("nutrition/goals/", { token });
  }

  async updateNutritionGoals(goals: Record<string, unknown>) {
    const token = Cookies.get("token");
    return this.post("nutrition/goals/", { ...goals, token });
  }

  // Basic Info POST endpoints (already have storeBasicInfo)
  async getBasicInfo() {
    const token = Cookies.get("token");
    return this.post("basic-info/get/", { token });
  }

  async updateBasicInfo(data: Record<string, unknown>) {
    const token = Cookies.get("token");
    return this.post("basic-info/update/", { ...data, token });
  }

  // Health Profile POST endpoints (already have storeHealthProfile)
  async getHealthProfile() {
    const token = Cookies.get("token");
    return this.post("health-profile/get/", { token });
  }

  async updateHealthProfile(data: Record<string, unknown>) {
    const token = Cookies.get("token");
    return this.post("health-profile/update/", { ...data, token });
  }
}

export const apiClient = new ApiClient();
