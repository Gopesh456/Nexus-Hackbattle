import React, { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { Heart, Settings, LogOut, Calendar, RefreshCw } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { RealtimeHealthMetrics } from "../components/dashboard/RealtimeHealthMetrics";
import { DailyNutritionSummary } from "../components/dashboard/DailyNutritionSummary";
import { FoodDiary } from "../components/dashboard/FoodDiary";

export const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [refreshKey, setRefreshKey] = useState(0);

  const handleRefresh = useCallback(() => {
    setRefreshKey((prev) => prev + 1);
  }, []);

  const handleUpdateSummary = useCallback(() => {
    // This will trigger a re-render of components that depend on nutrition data
    setRefreshKey((prev) => prev + 1);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      {/* Enhanced Header */}
      <header className="bg-white shadow-lg border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <motion.div
                whileHover={{ scale: 1.1, rotate: 10 }}
                className="w-12 h-12 bg-gradient-to-br from-[#76B3A8] to-[#5A9A8E] rounded-xl flex items-center justify-center shadow-lg"
              >
                <Heart className="w-7 h-7 text-white" />
              </motion.div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Nexus Health
                </h1>
                <p className="text-sm text-gray-600">
                  Welcome back, {user?.user}
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              {/* Current Date Display */}
              <div className="flex items-center space-x-2 px-4 py-2 bg-gray-100 rounded-xl mr-4">
                <Calendar className="w-4 h-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">
                  {new Date().toLocaleDateString("en-US", {
                    weekday: "short",
                    month: "short",
                    day: "numeric",
                  })}
                </span>
              </div>

              {/* Action Buttons */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleRefresh}
                className="p-3 text-gray-600 hover:text-[#76B3A8] hover:bg-[#76B3A8]/10 rounded-xl transition-all duration-200"
                title="Refresh all data"
              >
                <RefreshCw className="w-5 h-5" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-3 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-xl transition-all duration-200"
                title="Settings"
              >
                <Settings className="w-5 h-5" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={logout}
                className="p-3 text-gray-600 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all duration-200"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </motion.button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Dashboard Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Real-time Health Metrics Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            key={`metrics-${refreshKey}`}
          >
            <RealtimeHealthMetrics />
          </motion.div>

          {/* Daily Nutrition Overview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            key={`nutrition-${refreshKey}`}
          >
            <DailyNutritionSummary />
          </motion.div>

          {/* Food Diary Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            key={`diary-${refreshKey}`}
          >
            <FoodDiary onUpdateSummary={handleUpdateSummary} />
          </motion.div>
        </div>

        {/* Quick Stats Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-12 text-center py-8 border-t border-gray-200"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-[#76B3A8] mb-1">
                {new Date().toLocaleDateString("en-US", { day: "numeric" })}
              </div>
              <div className="text-sm text-gray-600">Days Active</div>
            </div>

            <div className="text-center">
              <div className="text-3xl font-bold text-blue-500 mb-1">24/7</div>
              <div className="text-sm text-gray-600">Health Monitoring</div>
            </div>

            <div className="text-center">
              <div className="text-3xl font-bold text-green-500 mb-1">Live</div>
              <div className="text-sm text-gray-600">Data Sync</div>
            </div>
          </div>

          <p className="text-xs text-gray-500 mt-6">
            Data updates every 5 seconds • Powered by advanced health sensors
            and AI nutrition analysis
          </p>
        </motion.div>
      </main>
    </div>
  );
};
