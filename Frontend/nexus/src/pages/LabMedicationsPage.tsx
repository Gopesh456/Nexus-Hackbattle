import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FlaskConical, Pill, ScanLine, Plus } from "lucide-react";
import { LabReportsTab } from "../components/lab-medications/LabReportsTab";
import { MedicationsTab } from "../components/lab-medications/MedicationsTab";

export const LabMedicationsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"lab-reports" | "medications">(
    "lab-reports"
  );

  return (
    <div className="p-6">
      {/* Header Section */}
      <div className="mb-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-2"
        >
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <FlaskConical className="w-8 h-8 text-[#76B3A8]" />
              <Pill className="w-8 h-8 text-[#76B3A8]" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900">
              Labs & Medications
            </h1>
          </div>

          {/* Utility Buttons */}
          <div className="flex items-center space-x-3">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center space-x-2 bg-white text-[#76B3A8] border-2 border-[#76B3A8] px-4 py-2 rounded-lg hover:bg-[#76B3A8] hover:text-white transition-all"
            >
              <ScanLine className="w-5 h-5" />
              <span>Scan Report</span>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center space-x-2 bg-[#76B3A8] text-white px-4 py-2 rounded-lg hover:bg-[#6ba396] transition-all"
            >
              <Plus className="w-5 h-5" />
              <span>Add Medication</span>
            </motion.button>
          </div>
        </motion.div>
        <p className="text-gray-600">
          Manage your lab reports and medications in one place
        </p>
      </div>

      {/* Tab Switcher */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="mb-6"
      >
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg w-fit">
          <button
            onClick={() => setActiveTab("lab-reports")}
            className={`flex items-center space-x-2 px-6 py-3 rounded-md text-sm font-medium transition-all ${
              activeTab === "lab-reports"
                ? "bg-white text-[#76B3A8] shadow-sm"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            <FlaskConical className="w-4 h-4" />
            <span>Lab Reports</span>
          </button>

          <button
            onClick={() => setActiveTab("medications")}
            className={`flex items-center space-x-2 px-6 py-3 rounded-md text-sm font-medium transition-all ${
              activeTab === "medications"
                ? "bg-white text-[#76B3A8] shadow-sm"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            <Pill className="w-4 h-4" />
            <span>Medications</span>
          </button>
        </div>
      </motion.div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.2 }}
        >
          {activeTab === "lab-reports" ? <LabReportsTab /> : <MedicationsTab />}
        </motion.div>
      </AnimatePresence>
    </div>
  );
};
