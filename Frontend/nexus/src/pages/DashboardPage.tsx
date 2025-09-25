import React from "react";
import { motion } from "framer-motion";
import { Activity, Heart, TrendingUp, Calendar } from "lucide-react";
import { RealtimeHealthMetrics } from "../components/dashboard/RealtimeHealthMetrics";
import { DailyNutritionSummary } from "../components/dashboard/DailyNutritionSummary";

export const DashboardPage: React.FC = () => {
  return (
    <div className="p-6">
      {/* Page Header */}
      <div className="mb-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center space-x-3 mb-2"
        >
          <Activity className="w-8 h-8 text-[#76B3A8]" />
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        </motion.div>
        <p className="text-gray-600">
          Your health overview and real-time metrics
        </p>
      </div>

      {/* Quick Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl p-6 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100">Heart Rate</p>
              <p className="text-2xl font-bold">72 BPM</p>
            </div>
            <Heart className="w-8 h-8 text-blue-200" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-6 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100">Steps Today</p>
              <p className="text-2xl font-bold">8,432</p>
            </div>
            <TrendingUp className="w-8 h-8 text-green-200" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl p-6 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100">Sleep Quality</p>
              <p className="text-2xl font-bold">8.5/10</p>
            </div>
            <Calendar className="w-8 h-8 text-purple-200" />
          </div>
        </motion.div>
      </div>

      {/* Main Dashboard Components */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
        >
          <RealtimeHealthMetrics />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <DailyNutritionSummary />
        </motion.div>
      </div>
    </div>
  );
};
