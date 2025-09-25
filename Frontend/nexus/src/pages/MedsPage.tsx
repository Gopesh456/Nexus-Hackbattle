import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  Pill,
  Plus,
  Clock,
  AlertTriangle,
  CheckCircle,
  Calendar,
} from "lucide-react";

interface Medication {
  id: string;
  name: string;
  dosage: string;
  frequency: string;
  timeSlots: string[];
  taken: boolean[];
  prescribedBy: string;
  startDate: string;
  endDate?: string;
  instructions: string;
}

export const MedsPage: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState(
    new Date().toISOString().split("T")[0]
  );

  const medications: Medication[] = [
    {
      id: "1",
      name: "Lisinopril",
      dosage: "10mg",
      frequency: "Once daily",
      timeSlots: ["08:00"],
      taken: [true],
      prescribedBy: "Dr. Smith",
      startDate: "2025-09-01",
      instructions: "Take with water, preferably in the morning",
    },
    {
      id: "2",
      name: "Metformin",
      dosage: "500mg",
      frequency: "Twice daily",
      timeSlots: ["08:00", "20:00"],
      taken: [true, false],
      prescribedBy: "Dr. Johnson",
      startDate: "2025-08-15",
      instructions: "Take with meals to reduce stomach upset",
    },
    {
      id: "3",
      name: "Vitamin D3",
      dosage: "1000 IU",
      frequency: "Once daily",
      timeSlots: ["08:00"],
      taken: [false],
      prescribedBy: "Dr. Smith",
      startDate: "2025-09-10",
      instructions: "Take with food for better absorption",
    },
  ];

  const toggleMedication = (medId: string, timeIndex: number) => {
    // In a real app, this would update the medication status
    console.log(`Toggling medication ${medId} at time index ${timeIndex}`);
  };

  const getTodayStats = () => {
    const totalDoses = medications.reduce(
      (sum, med) => sum + med.timeSlots.length,
      0
    );
    const takenDoses = medications.reduce(
      (sum, med) => sum + med.taken.filter((t) => t).length,
      0
    );
    return { totalDoses, takenDoses };
  };

  const { totalDoses, takenDoses } = getTodayStats();
  const adherenceRate = Math.round((takenDoses / totalDoses) * 100);

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
            <Pill className="w-8 h-8 text-[#76B3A8]" />
            <h1 className="text-3xl font-bold text-gray-900">Medications</h1>
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center space-x-2 bg-[#76B3A8] text-white px-4 py-2 rounded-lg hover:bg-[#6ba396] transition-all"
          >
            <Plus className="w-5 h-5" />
            <span>Add Medication</span>
          </motion.button>
        </motion.div>
        <p className="text-gray-600">
          Manage your medications and track adherence
        </p>
      </div>

      {/* Date Selector */}
      <div className="mb-6">
        <div className="flex items-center space-x-3">
          <Calendar className="w-5 h-5 text-gray-500" />
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
          />
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl p-6 border border-gray-200"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Today's Adherence</p>
              <p
                className={`text-2xl font-bold ${
                  adherenceRate >= 80 ? "text-green-600" : "text-red-600"
                }`}
              >
                {adherenceRate}%
              </p>
              <p className="text-xs text-gray-500">
                {takenDoses} of {totalDoses} doses
              </p>
            </div>
            {adherenceRate >= 80 ? (
              <CheckCircle className="w-8 h-8 text-green-500" />
            ) : (
              <AlertTriangle className="w-8 h-8 text-red-500" />
            )}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl p-6 border border-gray-200"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Active Medications</p>
              <p className="text-2xl font-bold text-blue-600">
                {medications.length}
              </p>
            </div>
            <Pill className="w-8 h-8 text-blue-500" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl p-6 border border-gray-200"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Next Dose</p>
              <p className="text-2xl font-bold text-purple-600">2:30 PM</p>
              <p className="text-xs text-gray-500">Metformin 500mg</p>
            </div>
            <Clock className="w-8 h-8 text-purple-500" />
          </div>
        </motion.div>
      </div>

      {/* Medications List */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="space-y-4"
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Today's Schedule
        </h2>

        {medications.map((medication, index) => (
          <motion.div
            key={medication.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 * index }}
            className="bg-white rounded-xl p-6 border border-gray-200"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <Pill className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {medication.name}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {medication.dosage} • {medication.frequency}
                  </p>
                  <p className="text-xs text-gray-400">
                    Prescribed by {medication.prescribedBy}
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">
                {medication.instructions}
              </p>
            </div>

            <div className="flex flex-wrap gap-2">
              {medication.timeSlots.map((time, timeIndex) => (
                <motion.button
                  key={timeIndex}
                  onClick={() => toggleMedication(medication.id, timeIndex)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                    medication.taken[timeIndex]
                      ? "bg-green-100 text-green-700 border border-green-200"
                      : "bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200"
                  }`}
                >
                  <Clock className="w-4 h-4" />
                  <span>{time}</span>
                  {medication.taken[timeIndex] && (
                    <CheckCircle className="w-4 h-4 text-green-600" />
                  )}
                </motion.button>
              ))}
            </div>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
};
