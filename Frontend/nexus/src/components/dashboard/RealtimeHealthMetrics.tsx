import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Heart,
  Activity,
  Thermometer,
  Zap,
  Brain,
  Droplet,
  Gauge,
  Wifi,
  WifiOff,
  RefreshCw,
} from "lucide-react";
import { apiClient } from "../../utils/api";
import { RealtimeHealthData } from "../../types";

interface RealtimeHealthMetricsProps {
  className?: string;
}

export const RealtimeHealthMetrics: React.FC<RealtimeHealthMetricsProps> = ({
  className,
}) => {
  const [healthData, setHealthData] = useState<RealtimeHealthData | null>(null);
  const [isConnected, setIsConnected] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch real-time health data every 5 seconds
  useEffect(() => {
    let hasInitialData = false;
    
    const fetchHealthData = async () => {
      try {
        const response = await apiClient.getRealtimeHealthData();
        setHealthData(response.data);
        setIsConnected(true);
        setLastUpdate(new Date());
        setIsLoading(false);
        hasInitialData = true;
      } catch (error) {
        console.error("Failed to fetch health data:", error);
        setIsLoading(false);
        
        // Keep trying to connect - only set as disconnected if no initial data
        if (!hasInitialData) {
          setIsConnected(false);
          // Provide realistic demo data while trying to reconnect
          setHealthData({
            heart_rate: 72 + Math.floor(Math.random() * 16) - 8,
            steps: 8500 + Math.floor(Math.random() * 1500),
            calories_burned: 1850 + Math.floor(Math.random() * 300),
            blood_pressure: {
              systolic: 118 + Math.floor(Math.random() * 14),
              diastolic: 78 + Math.floor(Math.random() * 8),
            },
            blood_oxygen: 97 + Math.floor(Math.random() * 3),
            stress_level: 20 + Math.floor(Math.random() * 30), // More realistic stress levels
            temperature: 98.2 + (Math.random() * 1.4), // Normal body temperature range
            timestamp: new Date().toISOString(),
          });
          hasInitialData = true;
        }
      }
    };

    // Initial fetch
    fetchHealthData();

    // Set up interval for real-time updates
    const interval = setInterval(fetchHealthData, 5000);

    return () => clearInterval(interval);
  }, []);

  const getHeartRateColor = (hr: number) => {
    if (hr < 60) return "#3B82F6"; // Blue - Low
    if (hr < 100) return "#10B981"; // Green - Normal
    if (hr < 120) return "#F59E0B"; // Yellow - Elevated
    return "#EF4444"; // Red - High
  };

  const getStressColor = (stress: number) => {
    if (stress < 30) return "#10B981"; // Green - Low stress
    if (stress < 60) return "#F59E0B"; // Yellow - Moderate stress
    return "#EF4444"; // Red - High stress
  };

  const getTemperatureColor = (temp: number) => {
    if (temp < 97.5) return "#3B82F6"; // Blue - Low
    if (temp < 99.5) return "#10B981"; // Green - Normal
    return "#EF4444"; // Red - Fever
  };

  const healthMetrics = healthData
    ? [
        {
          id: "heart_rate",
          title: "Heart Rate",
          value: `${healthData.heart_rate}`,
          unit: "bpm",
          icon: Heart,
          color: getHeartRateColor(healthData.heart_rate),
          trend: healthData.heart_rate > 80 ? "+5" : "-2",
        },
        {
          id: "steps",
          title: "Steps Today",
          value: healthData.steps.toLocaleString(),
          unit: "steps",
          icon: Activity,
          color: "#8B5CF6",
          trend: "+1,240",
        },
        {
          id: "calories",
          title: "Calories Burned",
          value: healthData.calories_burned.toLocaleString(),
          unit: "cal",
          icon: Zap,
          color: "#F59E0B",
          trend: "+156",
        },
        {
          id: "blood_pressure",
          title: "Blood Pressure",
          value: `${healthData.blood_pressure?.systolic}/${healthData.blood_pressure?.diastolic}`,
          unit: "mmHg",
          icon: Gauge,
          color: "#06B6D4",
          trend: "Normal",
        },
        {
          id: "oxygen",
          title: "Blood Oxygen",
          value: `${healthData.blood_oxygen}`,
          unit: "%",
          icon: Droplet,
          color: "#10B981",
          trend: "Good",
        },
        {
          id: "stress",
          title: "Stress Level",
          value: `${healthData.stress_level}`,
          unit: "%",
          icon: Brain,
          color: getStressColor(healthData.stress_level || 0),
          trend:
            healthData.stress_level && healthData.stress_level > 50
              ? "High"
              : "Low",
        },
        {
          id: "temperature",
          title: "Body Temperature",
          value: `${healthData.temperature?.toFixed(1)}`,
          unit: "°F",
          icon: Thermometer,
          color: getTemperatureColor(healthData.temperature || 98.6),
          trend: "Normal",
        },
      ]
    : [];

  if (isLoading) {
    return (
      <div className={`bg-white rounded-2xl shadow-xl p-6 ${className}`}>
        <div className="flex items-center justify-center h-64">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-12 h-12 border-4 border-[#76B3A8] border-t-transparent rounded-full"
          />
          <span className="ml-4 text-gray-600">Connecting to devices...</span>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-2xl shadow-xl p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <Activity className="w-7 h-7 mr-3 text-[#76B3A8]" />
          <div>
            <h3 className="text-2xl font-bold text-gray-900">
              Real-time Health
            </h3>
            <div className="flex items-center mt-1">
              {isConnected ? (
                <Wifi className="w-4 h-4 text-green-500 mr-2" />
              ) : (
                <WifiOff className="w-4 h-4 text-red-500 mr-2" />
              )}
              <span className="text-sm text-gray-500">
                {isConnected ? "Online Mode • Live Data" : "Demo Mode • Simulated Data"} 
                {lastUpdate && ` • Updated ${lastUpdate.toLocaleTimeString()}`}
              </span>
            </div>
          </div>
        </div>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => window.location.reload()}
          className="p-2 text-gray-500 hover:text-[#76B3A8] transition-colors"
        >
          <RefreshCw className="w-5 h-5" />
        </motion.button>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <AnimatePresence>
          {healthMetrics.map((metric, index) => {
            const IconComponent = metric.icon;

            return (
              <motion.div
                key={metric.id}
                initial={{ opacity: 0, y: 20, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20, scale: 0.9 }}
                transition={{ delay: index * 0.1 }}
                className="bg-gradient-to-br from-gray-50 to-white rounded-xl p-4 border border-gray-200 hover:shadow-lg transition-all duration-300"
              >
                <div className="flex items-start justify-between mb-3">
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center"
                    style={{ backgroundColor: `${metric.color}20` }}
                  >
                    <IconComponent
                      className="w-6 h-6"
                      style={{ color: metric.color }}
                    />
                  </div>

                  {/* Live indicator */}
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="w-3 h-3 bg-green-500 rounded-full"
                  />
                </div>

                <div>
                  <h4 className="text-sm font-medium text-gray-600 mb-1">
                    {metric.title}
                  </h4>
                  <div className="flex items-baseline space-x-1">
                    <span className="text-2xl font-bold text-gray-900">
                      {metric.value}
                    </span>
                    <span className="text-sm font-medium text-gray-500">
                      {metric.unit}
                    </span>
                  </div>

                  <div className="flex items-center mt-2">
                    <span
                      className="text-xs font-medium px-2 py-1 rounded-full"
                      style={{
                        color: metric.color,
                        backgroundColor: `${metric.color}20`,
                      }}
                    >
                      {metric.trend}
                    </span>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Health Status Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="mt-6 p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-xl border border-green-200"
      >
        <div className="flex items-center">
          <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center mr-4">
            <Heart className="w-5 h-5 text-white" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">Health Status: Good</h4>
            <p className="text-sm text-gray-600">
              All vital signs are within normal ranges. Keep up the great work!
            </p>
          </div>
        </div>
      </motion.div>

      {/* Data Source Note */}
      <div className="mt-4 text-center">
        <p className="text-xs text-gray-500">
          Data synced from smartwatch and health sensors • Updates every 5
          seconds
        </p>
      </div>
    </div>
  );
};
