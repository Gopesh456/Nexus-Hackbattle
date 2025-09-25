import React from "react";
import { motion } from "framer-motion";
import { Utensils, PlusCircle } from "lucide-react";
import { FoodDiary } from "../components/dashboard/FoodDiary";

export const FoodDiaryPage: React.FC = () => {
  return (
    <div className="p-6">
      {/* Page Header */}
      <div className="mb-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-2"
        >
          <div className="flex items-center space-x-3">
            <Utensils className="w-8 h-8 text-[#76B3A8]" />
            <h1 className="text-3xl font-bold text-gray-900">Food Diary</h1>
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center space-x-2 bg-[#76B3A8] text-white px-4 py-2 rounded-lg hover:bg-[#6ba396] transition-all"
          >
            <PlusCircle className="w-5 h-5" />
            <span>Quick Add</span>
          </motion.button>
        </motion.div>
        <p className="text-gray-600">Track your meals and nutrition intake</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl p-4 border border-gray-200"
        >
          <div className="text-center">
            <p className="text-sm text-gray-500">Today's Calories</p>
            <p className="text-2xl font-bold text-gray-900">1,847</p>
            <p className="text-xs text-green-600">350 remaining</p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl p-4 border border-gray-200"
        >
          <div className="text-center">
            <p className="text-sm text-gray-500">Protein</p>
            <p className="text-2xl font-bold text-blue-600">78g</p>
            <p className="text-xs text-gray-500">of 120g goal</p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl p-4 border border-gray-200"
        >
          <div className="text-center">
            <p className="text-sm text-gray-500">Carbs</p>
            <p className="text-2xl font-bold text-orange-600">185g</p>
            <p className="text-xs text-gray-500">of 200g goal</p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-xl p-4 border border-gray-200"
        >
          <div className="text-center">
            <p className="text-sm text-gray-500">Water</p>
            <p className="text-2xl font-bold text-blue-500">1.8L</p>
            <p className="text-xs text-gray-500">of 2.5L goal</p>
          </div>
        </motion.div>
      </div>

      {/* Food Diary Component */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <FoodDiary onUpdateSummary={() => {}} />
      </motion.div>
    </div>
  );
};
