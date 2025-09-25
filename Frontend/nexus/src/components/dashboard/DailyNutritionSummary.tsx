import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Target,
  TrendingUp,
  Clock,
  Flame,
  Beef,
  Wheat,
  Droplets,
  Award,
  AlertCircle,
  CheckCircle,
} from "lucide-react";
import { apiClient } from "../../utils/api";
import { DailyNutritionSummary as NutritionSummaryType } from "../../types";

interface DailyNutritionSummaryProps {
  className?: string;
}

export const DailyNutritionSummary: React.FC<DailyNutritionSummaryProps> = ({
  className,
}) => {
  const [summaryData, setSummaryData] = useState<NutritionSummaryType | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDailySummary();
  }, []);

  const fetchDailySummary = async () => {
    try {
      const response = await apiClient.getDailySummary();
      setSummaryData(response.data);
    } catch (error) {
      console.error("Failed to fetch daily summary:", error);
      // Mock data for demonstration
      setSummaryData({
        total_calories: 1650,
        total_protein: 85,
        total_carbs: 180,
        total_fat: 65,
        goal_calories: 2200,
        goal_protein: 110,
        goal_carbs: 275,
        goal_fat: 73,
        meals: {
          breakfast: { calories: 420, items: 3 },
          lunch: { calories: 680, items: 4 },
          dinner: { calories: 550, items: 3 },
          snack: { calories: 0, items: 0 },
        },
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading || !summaryData) {
    return (
      <div className={`bg-white rounded-2xl shadow-xl p-6 ${className}`}>
        <div className="flex items-center justify-center h-48">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-8 h-8 border-4 border-[#76B3A8] border-t-transparent rounded-full"
          />
          <span className="ml-3 text-gray-600">
            Loading nutrition summary...
          </span>
        </div>
      </div>
    );
  }

  const caloriesPercent =
    (summaryData.total_calories / summaryData.goal_calories) * 100;
  const proteinPercent =
    (summaryData.total_protein / summaryData.goal_protein) * 100;
  const carbsPercent = (summaryData.total_carbs / summaryData.goal_carbs) * 100;
  const fatPercent = (summaryData.total_fat / summaryData.goal_fat) * 100;

  const remainingCalories =
    summaryData.goal_calories - summaryData.total_calories;

  const macronutrients = [
    {
      name: "Protein",
      current: summaryData.total_protein,
      goal: summaryData.goal_protein,
      unit: "g",
      color: "#3B82F6",
      icon: Beef,
      percent: proteinPercent,
    },
    {
      name: "Carbs",
      current: summaryData.total_carbs,
      goal: summaryData.goal_carbs,
      unit: "g",
      color: "#10B981",
      icon: Wheat,
      percent: carbsPercent,
    },
    {
      name: "Fat",
      current: summaryData.total_fat,
      goal: summaryData.goal_fat,
      unit: "g",
      color: "#F59E0B",
      icon: Droplets,
      percent: fatPercent,
    },
  ];

  const getStatusColor = (percent: number) => {
    if (percent < 50) return "#EF4444"; // Red - Low
    if (percent < 80) return "#F59E0B"; // Yellow - Moderate
    if (percent <= 110) return "#10B981"; // Green - Good
    return "#F59E0B"; // Yellow - Over
  };

  const getStatusIcon = (percent: number) => {
    if (percent < 50) return AlertCircle;
    if (percent <= 110) return CheckCircle;
    return AlertCircle;
  };

  return (
    <div className={`bg-white rounded-2xl shadow-xl p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <Target className="w-7 h-7 mr-3 text-[#76B3A8]" />
          <div>
            <h3 className="text-2xl font-bold text-gray-900">Daily Overview</h3>
            <p className="text-sm text-gray-500">
              {new Date().toLocaleDateString("en-US", {
                weekday: "long",
                month: "long",
                day: "numeric",
              })}
            </p>
          </div>
        </div>

        <motion.div
          whileHover={{ scale: 1.05 }}
          className="flex items-center px-4 py-2 bg-gradient-to-r from-[#76B3A8] to-[#5A9A8E] text-white rounded-xl"
        >
          <Award className="w-5 h-5 mr-2" />
          <span className="font-medium">
            {caloriesPercent >= 80 ? "On Track!" : "Keep Going!"}
          </span>
        </motion.div>
      </div>

      {/* Calories Progress */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-lg font-semibold text-gray-900 flex items-center">
            <Flame className="w-5 h-5 mr-2 text-orange-500" />
            Calories
          </h4>
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-900">
              {summaryData.total_calories.toLocaleString()}
            </div>
            <div className="text-sm text-gray-500">
              of {summaryData.goal_calories.toLocaleString()} goal
            </div>
          </div>
        </div>

        {/* Calories Progress Bar */}
        <div className="relative">
          <div className="w-full bg-gray-200 rounded-full h-4">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${Math.min(caloriesPercent, 100)}%` }}
              transition={{ duration: 1, delay: 0.2 }}
              className="bg-gradient-to-r from-orange-400 to-red-500 h-4 rounded-full relative overflow-hidden"
            >
              <motion.div
                animate={{ x: [-20, 100, -20] }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12"
              />
            </motion.div>
          </div>

          <div className="flex justify-between mt-2 text-sm">
            <span className="text-gray-600">
              {Math.round(caloriesPercent)}% of goal
            </span>
            <span
              className={`font-medium ${
                remainingCalories > 0 ? "text-[#76B3A8]" : "text-orange-600"
              }`}
            >
              {remainingCalories > 0
                ? `${remainingCalories} cal remaining`
                : `${Math.abs(remainingCalories)} cal over goal`}
            </span>
          </div>
        </div>
      </div>

      {/* Macronutrients */}
      <div className="mb-8">
        <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <TrendingUp className="w-5 h-5 mr-2 text-[#76B3A8]" />
          Macronutrients
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {macronutrients.map((macro, index) => {
            const IconComponent = macro.icon;
            const StatusIcon = getStatusIcon(macro.percent);

            return (
              <motion.div
                key={macro.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className="bg-gradient-to-br from-gray-50 to-white rounded-xl p-4 border border-gray-200"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center">
                    <div
                      className="w-10 h-10 rounded-lg flex items-center justify-center"
                      style={{ backgroundColor: `${macro.color}20` }}
                    >
                      <IconComponent
                        className="w-5 h-5"
                        style={{ color: macro.color }}
                      />
                    </div>
                    <span className="ml-3 font-medium text-gray-900">
                      {macro.name}
                    </span>
                  </div>

                  <StatusIcon
                    className="w-5 h-5"
                    style={{ color: getStatusColor(macro.percent) }}
                  />
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">
                      {macro.current}
                      {macro.unit}
                    </span>
                    <span className="text-gray-500">
                      of {macro.goal}
                      {macro.unit}
                    </span>
                  </div>

                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.min(macro.percent, 100)}%` }}
                      transition={{ duration: 1, delay: 0.5 + index * 0.1 }}
                      className="h-2 rounded-full"
                      style={{ backgroundColor: macro.color }}
                    />
                  </div>

                  <div
                    className="text-center text-xs font-medium"
                    style={{ color: macro.color }}
                  >
                    {Math.round(macro.percent)}%
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Meal Breakdown */}
      <div>
        <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Clock className="w-5 h-5 mr-2 text-[#76B3A8]" />
          Today's Meals
        </h4>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          {Object.entries(summaryData.meals).map(
            ([mealType, mealData], index) => {
              const mealColors = {
                breakfast: "#F59E0B",
                lunch: "#10B981",
                dinner: "#8B5CF6",
                snack: "#F97316",
              };

              return (
                <motion.div
                  key={mealType}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.6 + index * 0.1 }}
                  className="text-center p-4 bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-200"
                >
                  <div
                    className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-2"
                    style={{
                      backgroundColor: `${
                        mealColors[mealType as keyof typeof mealColors]
                      }20`,
                    }}
                  >
                    <span
                      className="text-xl font-bold"
                      style={{
                        color: mealColors[mealType as keyof typeof mealColors],
                      }}
                    >
                      {mealData.calories}
                    </span>
                  </div>

                  <h5 className="font-medium text-gray-900 capitalize mb-1">
                    {mealType}
                  </h5>
                  <p className="text-xs text-gray-600">
                    {mealData.items} items
                  </p>
                  <p className="text-xs text-gray-500">calories</p>
                </motion.div>
              );
            }
          )}
        </div>
      </div>
    </div>
  );
};
