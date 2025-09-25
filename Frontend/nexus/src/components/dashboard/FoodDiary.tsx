import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Plus,
  Mic,
  Edit3,
  Trash2,
  Clock,
  CheckCircle2,
  X,
  Search,
  Utensils,
  Coffee,
  Sun,
  Moon as MoonIcon,
  Cookie,
} from "lucide-react";
import { apiClient } from "../../utils/api";
import { FoodLog, NutritionDetails } from "../../types";

interface FoodDiaryProps {
  onUpdateSummary: () => void;
}

const mealIcons = {
  breakfast: Coffee,
  lunch: Sun,
  dinner: MoonIcon,
  snack: Cookie,
};

const mealColors = {
  breakfast: "#F59E0B",
  lunch: "#10B981",
  dinner: "#8B5CF6",
  snack: "#F97316",
};

export const FoodDiary: React.FC<FoodDiaryProps> = ({ onUpdateSummary }) => {
  const [foodLogs, setFoodLogs] = useState<FoodLog[]>([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [selectedMeal, setSelectedMeal] = useState<
    "breakfast" | "lunch" | "dinner" | "snack"
  >("breakfast");
  const [isVoiceMode, setIsVoiceMode] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showNutrition, setShowNutrition] = useState(false);
  const [editingFood, setEditingFood] = useState<FoodLog | null>(null);

  const [formData, setFormData] = useState({
    food_name: "",
    quantity: "",
    unit: "g",
    time: new Date().toTimeString().slice(0, 5), // HH:MM format
  });

  const [nutritionData, setNutritionData] = useState<NutritionDetails | null>(
    null
  );

  const units = ["g", "kg", "oz", "lb", "cup", "ml", "l"];
  const meals = ["breakfast", "lunch", "dinner", "snack"] as const;

  useEffect(() => {
    loadFoodLogs();
  }, []);

  const loadFoodLogs = async () => {
    try {
      const response = await apiClient.getNutritionHistory();
      setFoodLogs(response.data || []);
    } catch (error) {
      console.error("Failed to load food logs:", error);
    }
  };

  const handleVoiceInput = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Speech recognition not supported in this browser");
      return;
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      setIsVoiceMode(true);
    };

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setFormData((prev) => ({ ...prev, food_name: transcript }));
      setIsVoiceMode(false);
    };

    recognition.onerror = () => {
      setIsVoiceMode(false);
      alert("Voice recognition failed. Please try again.");
    };

    recognition.onend = () => {
      setIsVoiceMode(false);
    };

    recognition.start();
  };

  const fetchNutritionData = async () => {
    if (!formData.food_name || !formData.quantity) return;

    setIsLoading(true);
    try {
      const response = await apiClient.addFoodEntry(
        formData.food_name,
        parseFloat(formData.quantity),
        formData.unit,
        formData.time,
        selectedMeal
      );

      setNutritionData(response.nutrition);
      setShowNutrition(true);
    } catch (error) {
      console.error("Failed to fetch nutrition data:", error);
      alert("Failed to fetch nutrition data. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const logFood = async () => {
    if (!nutritionData) return;

    try {
      await loadFoodLogs();
      onUpdateSummary();
      resetForm();
      setShowAddForm(false);
      setShowNutrition(false);
    } catch (error) {
      console.error("Failed to log food:", error);
      alert("Failed to log food. Please try again.");
    }
  };

  const deleteFood = async (foodId: string) => {
    try {
      await apiClient.deleteNutritionEntry(parseInt(foodId));
      await loadFoodLogs();
      onUpdateSummary();
    } catch (error) {
      console.error("Failed to delete food:", error);
      alert("Failed to delete food. Please try again.");
    }
  };

  const editFood = (food: FoodLog) => {
    setEditingFood(food);
    setFormData({
      food_name: food.food_name,
      quantity: food.quantity.toString(),
      unit: food.unit,
      time: food.time,
    });
    setSelectedMeal(food.meal_type);
    setShowAddForm(true);
  };

  const saveEdit = async () => {
    if (!editingFood) return;

    try {
      await apiClient.editNutritionEntry(
        parseInt(editingFood.id),
        formData.food_name,
        parseFloat(formData.quantity),
        formData.unit,
        formData.time,
        selectedMeal
      );
      await loadFoodLogs();
      onUpdateSummary();
      resetForm();
      setEditingFood(null);
      setShowAddForm(false);
    } catch (error) {
      console.error("Failed to edit food:", error);
      alert("Failed to edit food. Please try again.");
    }
  };

  const resetForm = () => {
    setFormData({
      food_name: "",
      quantity: "",
      unit: "g",
      time: new Date().toTimeString().slice(0, 5),
    });
    setNutritionData(null);
    setShowNutrition(false);
    setEditingFood(null);
  };

  const getMealCalories = (mealType: string) => {
    return foodLogs
      .filter((food) => food.meal_type === mealType)
      .reduce((total, food) => total + food.nutrition.calories, 0);
  };

  const LoadingScreen = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
    >
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        className="w-16 h-16 border-4 border-[#76B3A8] border-t-transparent rounded-full"
      />
      <p className="ml-4 text-white text-lg font-medium">
        Analyzing nutrition...
      </p>
    </motion.div>
  );

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-gray-900 flex items-center">
          <Utensils className="w-7 h-7 mr-3 text-[#76B3A8]" />
          Food Diary
        </h3>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowAddForm(true)}
          className="flex items-center px-4 py-2 bg-[#76B3A8] text-white rounded-xl hover:bg-[#76B3A8]/80 transition-colors"
        >
          <Plus className="w-5 h-5 mr-2" />
          Add Food
        </motion.button>
      </div>

      {/* Meal Categories */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {meals.map((meal) => {
          const Icon = mealIcons[meal];
          const calories = getMealCalories(meal);

          return (
            <motion.div
              key={meal}
              whileHover={{ scale: 1.02 }}
              className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-4 border border-gray-200"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center">
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: mealColors[meal] }}
                  >
                    <Icon className="w-5 h-5 text-white" />
                  </div>
                </div>
                <span className="text-sm font-medium text-gray-600">
                  {calories} cal
                </span>
              </div>
              <h4 className="font-semibold text-gray-900 capitalize">{meal}</h4>
              <p className="text-sm text-gray-600">
                {foodLogs.filter((f) => f.meal_type === meal).length} items
              </p>
            </motion.div>
          );
        })}
      </div>

      {/* Food Log List */}
      <div className="space-y-3">
        {foodLogs.length === 0 ? (
          <div className="text-center py-12">
            <Utensils className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No food logged today</p>
            <p className="text-gray-400">Start by adding your first meal</p>
          </div>
        ) : (
          foodLogs.map((food) => {
            const Icon = mealIcons[food.meal_type as keyof typeof mealIcons];

            return (
              <motion.div
                key={food.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-200"
              >
                <div className="flex items-center space-x-4">
                  <div
                    className="w-12 h-12 rounded-lg flex items-center justify-center"
                    style={{
                      backgroundColor:
                        mealColors[food.meal_type as keyof typeof mealColors],
                    }}
                  >
                    <Icon className="w-6 h-6 text-white" />
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900">
                      {food.food_name}
                    </h4>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <span>
                        {food.quantity} {food.unit}
                      </span>
                      <span className="flex items-center">
                        <Clock className="w-4 h-4 mr-1" />
                        {food.time}
                      </span>
                      <span className="font-medium">
                        {food.nutrition.calories} cal
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => editFood(food)}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                  >
                    <Edit3 className="w-4 h-4" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => deleteFood(food.id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </motion.button>
                </div>
              </motion.div>
            );
          })
        )}
      </div>

      {/* Add/Edit Food Modal */}
      <AnimatePresence>
        {showAddForm && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-40 p-4"
            onClick={() => {
              setShowAddForm(false);
              resetForm();
            }}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold text-gray-900">
                  {editingFood ? "Edit Food" : "Add Food"}
                </h3>
                <button
                  onClick={() => {
                    setShowAddForm(false);
                    resetForm();
                  }}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>

              <div className="space-y-4">
                {/* Meal Type Selector */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Meal Type
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {meals.map((meal) => {
                      const Icon = mealIcons[meal];
                      return (
                        <button
                          key={meal}
                          onClick={() => setSelectedMeal(meal)}
                          className={`flex items-center justify-center p-3 rounded-lg border-2 transition-all ${
                            selectedMeal === meal
                              ? "border-[#76B3A8] bg-[#76B3A8]/10"
                              : "border-gray-200 hover:border-gray-300"
                          }`}
                        >
                          <Icon
                            className="w-4 h-4 mr-2"
                            style={{ color: mealColors[meal] }}
                          />
                          <span className="capitalize text-sm font-medium">
                            {meal}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Food Name Input */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Food Name
                  </label>
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={formData.food_name}
                      onChange={(e) =>
                        setFormData((prev) => ({
                          ...prev,
                          food_name: e.target.value,
                        }))
                      }
                      className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      placeholder="Enter food name"
                    />
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleVoiceInput}
                      className={`px-4 py-3 rounded-lg transition-colors ${
                        isVoiceMode
                          ? "bg-red-500 text-white"
                          : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                      }`}
                    >
                      <Mic className="w-5 h-5" />
                    </motion.button>
                  </div>
                </div>

                {/* Quantity and Unit */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Quantity
                    </label>
                    <input
                      type="number"
                      value={formData.quantity}
                      onChange={(e) =>
                        setFormData((prev) => ({
                          ...prev,
                          quantity: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      placeholder="100"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Unit
                    </label>
                    <select
                      value={formData.unit}
                      onChange={(e) =>
                        setFormData((prev) => ({
                          ...prev,
                          unit: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                    >
                      {units.map((unit) => (
                        <option key={unit} value={unit}>
                          {unit}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Time Input */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Time
                  </label>
                  <input
                    type="time"
                    value={formData.time}
                    onChange={(e) =>
                      setFormData((prev) => ({ ...prev, time: e.target.value }))
                    }
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                  />
                </div>

                {/* Get Nutrition Button */}
                {!showNutrition && !editingFood && (
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={fetchNutritionData}
                    disabled={!formData.food_name || !formData.quantity}
                    className="w-full py-3 bg-[#76B3A8] text-white rounded-lg font-medium hover:bg-[#76B3A8]/80 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                  >
                    <Search className="w-5 h-5 mr-2 inline" />
                    Get Nutrition Info
                  </motion.button>
                )}

                {/* Nutrition Display */}
                {showNutrition && nutritionData && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-gradient-to-br from-[#76B3A8]/10 to-[#76B3A8]/5 rounded-xl p-4 border border-[#76B3A8]/20"
                  >
                    <h4 className="font-semibold text-gray-900 mb-3">
                      Nutrition Facts
                    </h4>
                    <div className="grid grid-cols-2 gap-3">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-[#76B3A8]">
                          {nutritionData.calories}
                        </div>
                        <div className="text-xs text-gray-600">Calories</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">
                          {nutritionData.protein}g
                        </div>
                        <div className="text-xs text-gray-600">Protein</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">
                          {nutritionData.carbs}g
                        </div>
                        <div className="text-xs text-gray-600">Carbs</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-orange-600">
                          {nutritionData.fat}g
                        </div>
                        <div className="text-xs text-gray-600">Fat</div>
                      </div>
                    </div>

                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={logFood}
                      className="w-full mt-4 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center justify-center"
                    >
                      <CheckCircle2 className="w-5 h-5 mr-2" />
                      Log Food
                    </motion.button>
                  </motion.div>
                )}

                {/* Edit Food Actions */}
                {editingFood && (
                  <div className="flex space-x-3">
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => {
                        setShowAddForm(false);
                        resetForm();
                      }}
                      className="flex-1 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                    >
                      Cancel
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={saveEdit}
                      className="flex-1 py-3 bg-[#76B3A8] text-white rounded-lg font-medium hover:bg-[#76B3A8]/80 transition-colors"
                    >
                      Save Changes
                    </motion.button>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Loading Screen */}
      <AnimatePresence>{isLoading && <LoadingScreen />}</AnimatePresence>
    </div>
  );
};
