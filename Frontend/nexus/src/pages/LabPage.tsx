import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  FlaskConical,
  Download,
  Calendar,
  TrendingUp,
  AlertCircle,
} from "lucide-react";

interface LabResult {
  id: string;
  test: string;
  value: string;
  range: string;
  status: "normal" | "high" | "low";
  date: string;
}

export const LabPage: React.FC = () => {
  const [selectedPeriod, setSelectedPeriod] = useState("recent");

  const labResults: LabResult[] = [
    {
      id: "1",
      test: "Blood Glucose",
      value: "95 mg/dL",
      range: "70-100 mg/dL",
      status: "normal",
      date: "2025-09-20",
    },
    {
      id: "2",
      test: "Total Cholesterol",
      value: "220 mg/dL",
      range: "<200 mg/dL",
      status: "high",
      date: "2025-09-20",
    },
    {
      id: "3",
      test: "HDL Cholesterol",
      value: "45 mg/dL",
      range: ">40 mg/dL",
      status: "normal",
      date: "2025-09-20",
    },
    {
      id: "4",
      test: "LDL Cholesterol",
      value: "155 mg/dL",
      range: "<130 mg/dL",
      status: "high",
      date: "2025-09-20",
    },
    {
      id: "5",
      test: "Hemoglobin A1C",
      value: "5.4%",
      range: "<5.7%",
      status: "normal",
      date: "2025-09-18",
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "normal":
        return "text-green-600 bg-green-50";
      case "high":
        return "text-red-600 bg-red-50";
      case "low":
        return "text-yellow-600 bg-yellow-50";
      default:
        return "text-gray-600 bg-gray-50";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "normal":
        return "✓";
      case "high":
        return "↑";
      case "low":
        return "↓";
      default:
        return "?";
    }
  };

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
            <FlaskConical className="w-8 h-8 text-[#76B3A8]" />
            <h1 className="text-3xl font-bold text-gray-900">Lab Results</h1>
          </div>
          <div className="flex items-center space-x-3">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center space-x-2 bg-[#76B3A8] text-white px-4 py-2 rounded-lg hover:bg-[#6ba396] transition-all"
            >
              <Download className="w-5 h-5" />
              <span>Download Report</span>
            </motion.button>
          </div>
        </motion.div>
        <p className="text-gray-600">
          View and track your laboratory test results
        </p>
      </div>

      {/* Period Filter */}
      <div className="mb-6">
        <div className="flex space-x-2">
          {["recent", "3months", "6months", "year"].map((period) => (
            <button
              key={period}
              onClick={() => setSelectedPeriod(period)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                selectedPeriod === period
                  ? "bg-[#76B3A8] text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {period === "recent"
                ? "Recent"
                : period === "3months"
                ? "3 Months"
                : period === "6months"
                ? "6 Months"
                : "Year"}
            </button>
          ))}
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
              <p className="text-sm text-gray-500">Total Tests</p>
              <p className="text-2xl font-bold text-gray-900">
                {labResults.length}
              </p>
            </div>
            <Calendar className="w-8 h-8 text-blue-500" />
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
              <p className="text-sm text-gray-500">Normal Results</p>
              <p className="text-2xl font-bold text-green-600">
                {labResults.filter((r) => r.status === "normal").length}
              </p>
            </div>
            <TrendingUp className="w-8 h-8 text-green-500" />
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
              <p className="text-sm text-gray-500">Abnormal Results</p>
              <p className="text-2xl font-bold text-red-600">
                {labResults.filter((r) => r.status !== "normal").length}
              </p>
            </div>
            <AlertCircle className="w-8 h-8 text-red-500" />
          </div>
        </motion.div>
      </div>

      {/* Lab Results Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white rounded-xl border border-gray-200 overflow-hidden"
      >
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Recent Test Results
          </h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Test Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Result
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Reference Range
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {labResults.map((result, index) => (
                <motion.tr
                  key={result.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 * index }}
                  className="hover:bg-gray-50"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {result.test}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {result.value}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {result.range}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(
                        result.status
                      )}`}
                    >
                      {getStatusIcon(result.status)} {result.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(result.date).toLocaleDateString()}
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
};
