import React, { useState, useEffect, useRef, useCallback } from "react";
import { motion } from "framer-motion";
import {
  Heart,
  Activity,
  Flame,
  Droplets,
  Wind,
  Thermometer,
  Watch,
  Wifi,
  WifiOff,
  AlertTriangle,
} from "lucide-react";

interface HealthMetrics {
  heartRate: number;
  stepsToday: number;
  caloriesBurned: number;
  bloodPressure: {
    systolic: number;
    diastolic: number;
  };
  bloodOxygenLevel: number;
  stressLevel: number;
  bodyTemperature: number;
  timestamp?: string;
}

interface SmartWatchMetricsProps {
  className?: string;
}

export const SmartWatchMetrics: React.FC<SmartWatchMetricsProps> = ({ className = "" }) => {
  const [metrics, setMetrics] = useState<HealthMetrics>({
    heartRate: 0,
    stepsToday: 0,
    caloriesBurned: 0,
    bloodPressure: { systolic: 0, diastolic: 0 },
    bloodOxygenLevel: 0,
    stressLevel: 0,
    bodyTemperature: 0,
  });
  
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const WS_URL = "wss://jarrod-senescent-beatris.ngrok-free.dev";
  const HTTP_URL = "https://jarrod-senescent-beatris.ngrok-free.dev";

  const tryHttpPolling = useCallback(async () => {
    console.log("Attempting HTTP polling to:", HTTP_URL);
    setIsConnecting(true);
    setError(null);

    try {
      const response = await fetch(HTTP_URL, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'ngrok-skip-browser-warning': 'true'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log("HTTP polling successful, received data:", data);
        
        // Update metrics with received data
        setMetrics(prevMetrics => ({
          heartRate: data.heartRate || data.heart_rate || prevMetrics.heartRate,
          stepsToday: data.stepsToday || data.steps_today || data.steps || prevMetrics.stepsToday,
          caloriesBurned: data.caloriesBurned || data.calories_burned || data.calories || prevMetrics.caloriesBurned,
          bloodPressure: {
            systolic: data.bloodPressure?.systolic || data.blood_pressure?.systolic || data.systolic || prevMetrics.bloodPressure.systolic,
            diastolic: data.bloodPressure?.diastolic || data.blood_pressure?.diastolic || data.diastolic || prevMetrics.bloodPressure.diastolic,
          },
          bloodOxygenLevel: data.bloodOxygenLevel || data.blood_oxygen_level || data.oxygen || prevMetrics.bloodOxygenLevel,
          stressLevel: data.stressLevel || data.stress_level || data.stress || prevMetrics.stressLevel,
          bodyTemperature: data.bodyTemperature || data.body_temperature || data.temperature || prevMetrics.bodyTemperature,
          timestamp: data.timestamp || new Date().toISOString(),
        }));

        setLastUpdate(new Date());
        setIsConnected(true);
        setIsConnecting(false);
        
        // Set up polling interval for continuous updates
        pollingIntervalRef.current = setInterval(async () => {
          try {
            const pollResponse = await fetch(HTTP_URL, {
              method: 'GET',
              headers: {
                'Accept': 'application/json',
                'ngrok-skip-browser-warning': 'true'
              }
            });
            
            if (pollResponse.ok) {
              const pollData = await pollResponse.json();
              setMetrics(prevMetrics => ({
                heartRate: pollData.heartRate || pollData.heart_rate || prevMetrics.heartRate,
                stepsToday: pollData.stepsToday || pollData.steps_today || pollData.steps || prevMetrics.stepsToday,
                caloriesBurned: pollData.caloriesBurned || pollData.calories_burned || pollData.calories || prevMetrics.caloriesBurned,
                bloodPressure: {
                  systolic: pollData.bloodPressure?.systolic || pollData.blood_pressure?.systolic || pollData.systolic || prevMetrics.bloodPressure.systolic,
                  diastolic: pollData.bloodPressure?.diastolic || pollData.blood_pressure?.diastolic || pollData.diastolic || prevMetrics.bloodPressure.diastolic,
                },
                bloodOxygenLevel: pollData.bloodOxygenLevel || pollData.blood_oxygen_level || pollData.oxygen || prevMetrics.bloodOxygenLevel,
                stressLevel: pollData.stressLevel || pollData.stress_level || pollData.stress || prevMetrics.stressLevel,
                bodyTemperature: pollData.bodyTemperature || pollData.body_temperature || pollData.temperature || prevMetrics.bodyTemperature,
                timestamp: pollData.timestamp || new Date().toISOString(),
              }));
              setLastUpdate(new Date());
            }
          } catch (pollError) {
            console.error("HTTP polling error:", pollError);
          }
        }, 2000); // Poll every 2 seconds

      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      console.error("HTTP polling failed:", error);
      setError(`Connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      setIsConnecting(false);
      setIsConnected(false);
      
      // Retry HTTP polling after 5 seconds
      reconnectTimeoutRef.current = setTimeout(() => {
        tryHttpPolling();
      }, 5000);
    }
  }, [HTTP_URL]);

  const connectWebSocket = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    setIsConnecting(true);
    setError(null);

    console.log("Attempting to connect to:", WS_URL);

    try {
      wsRef.current = new WebSocket(WS_URL);

      wsRef.current.onopen = () => {
        console.log("SmartWatch WebSocket connected successfully");
        setIsConnected(true);
        setIsConnecting(false);
        setError(null);
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log("Received health data:", data);
          
          // Update metrics with received data
          setMetrics(prevMetrics => ({
            heartRate: data.heartRate || data.heart_rate || prevMetrics.heartRate,
            stepsToday: data.stepsToday || data.steps_today || data.steps || prevMetrics.stepsToday,
            caloriesBurned: data.caloriesBurned || data.calories_burned || data.calories || prevMetrics.caloriesBurned,
            bloodPressure: {
              systolic: data.bloodPressure?.systolic || data.blood_pressure?.systolic || data.systolic || prevMetrics.bloodPressure.systolic,
              diastolic: data.bloodPressure?.diastolic || data.blood_pressure?.diastolic || data.diastolic || prevMetrics.bloodPressure.diastolic,
            },
            bloodOxygenLevel: data.bloodOxygenLevel || data.blood_oxygen_level || data.oxygen || prevMetrics.bloodOxygenLevel,
            stressLevel: data.stressLevel || data.stress_level || data.stress || prevMetrics.stressLevel,
            bodyTemperature: data.bodyTemperature || data.body_temperature || data.temperature || prevMetrics.bodyTemperature,
            timestamp: data.timestamp || new Date().toISOString(),
          }));

          setLastUpdate(new Date());
        } catch (err) {
          console.error("Error parsing WebSocket data:", err);
        }
      };

      wsRef.current.onclose = (event) => {
        console.log("SmartWatch WebSocket disconnected. Code:", event.code, "Reason:", event.reason);
        setIsConnected(false);
        setIsConnecting(false);
        
        if (event.code !== 1000) { // Not a normal closure
          console.log("Abnormal closure, will try HTTP polling as fallback");
          setError("WebSocket failed. Trying HTTP polling...");
          // Try HTTP polling as fallback
          reconnectTimeoutRef.current = setTimeout(() => {
            tryHttpPolling();
          }, 2000);
        }
      };

      wsRef.current.onerror = (error) => {
        console.error("SmartWatch WebSocket error:", error);
        console.log("WebSocket connection failed, trying HTTP polling as fallback");
        setError("WebSocket failed. Trying HTTP polling...");
        setIsConnecting(false);
        setIsConnected(false);
        
        // Try HTTP polling as fallback after WebSocket fails
        setTimeout(() => {
          tryHttpPolling();
        }, 1000);
      };

    } catch (err) {
      console.error("WebSocket connection error:", err);
      setError("Failed to establish connection");
      setIsConnecting(false);
    }
  }, [tryHttpPolling]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
      pollingIntervalRef.current = null;
    }
    
    if (wsRef.current) {
      wsRef.current.close(1000, "Manual disconnect");
      wsRef.current = null;
    }
    
    setIsConnected(false);
    setIsConnecting(false);
    setError(null);
  }, []);

  useEffect(() => {
    connectWebSocket();

    return () => {
      disconnect();
    };
  }, [connectWebSocket, disconnect]);

  const getStatusColor = () => {
    if (isConnecting) return "text-yellow-600 bg-yellow-100 border-yellow-200";
    if (isConnected) return "text-green-600 bg-green-100 border-green-200";
    return "text-red-600 bg-red-100 border-red-200";
  };

  const getStatusIcon = () => {
    if (isConnecting) return <Activity className="w-4 h-4 animate-spin" />;
    if (isConnected) return <Wifi className="w-4 h-4" />;
    return <WifiOff className="w-4 h-4" />;
  };

  const getHealthStatus = (metric: keyof HealthMetrics, value: number | { systolic: number; diastolic: number }) => {
    switch (metric) {
      case 'heartRate': {
        const hr = value as number;
        if (hr < 60) return 'text-blue-600 bg-blue-50';
        if (hr > 100) return 'text-red-600 bg-red-50';
        return 'text-green-600 bg-green-50';
      }
      
      case 'bloodOxygenLevel': {
        const oxygen = value as number;
        if (oxygen < 95) return 'text-red-600 bg-red-50';
        return 'text-green-600 bg-green-50';
      }
      
      case 'stressLevel': {
        const stress = value as number;
        if (stress > 7) return 'text-red-600 bg-red-50';
        if (stress > 4) return 'text-yellow-600 bg-yellow-50';
        return 'text-green-600 bg-green-50';
      }
      
      case 'bodyTemperature': {
        const temp = value as number;
        if (temp > 99.5 || temp < 97) return 'text-red-600 bg-red-50';
        return 'text-green-600 bg-green-50';
      }
      
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header with Connection Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Watch className="w-6 h-6 text-[#76B3A8]" />
            <div>
              <h2 className="text-lg font-semibold text-gray-900">SmartWatch Health Metrics</h2>
              <p className="text-sm text-gray-600">Real-time health monitoring</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {lastUpdate && (
              <span className="text-xs text-gray-500">
                Last update: {lastUpdate.toLocaleTimeString()}
              </span>
            )}
            
            <div className={`flex items-center space-x-2 px-3 py-1 rounded-full border ${getStatusColor()}`}>
              {getStatusIcon()}
              <span className="text-sm font-medium">
                {isConnecting ? "Connecting..." : isConnected ? "Connected" : "Disconnected"}
              </span>
            </div>
            
            <div className="flex space-x-2">
              <button
                onClick={isConnected ? disconnect : connectWebSocket}
                disabled={isConnecting}
                className="px-3 py-1 text-sm bg-[#76B3A8] text-white rounded-lg hover:bg-[#6ba396] transition-colors disabled:opacity-50"
              >
                {isConnected ? "Disconnect" : "WebSocket"}
              </button>
              
              <button
                onClick={isConnected ? disconnect : tryHttpPolling}
                disabled={isConnecting}
                className="px-3 py-1 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {isConnected ? "Disconnect" : "HTTP Polling"}
              </button>
            </div>
          </div>
        </div>
        
        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-2"
          >
            <AlertTriangle className="w-4 h-4 text-red-600" />
            <span className="text-sm text-red-700">{error}</span>
          </motion.div>
        )}
      </motion.div>

      {/* Health Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Heart Rate */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-red-100 rounded-lg">
                <Heart className="w-6 h-6 text-red-600" />
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Heart Rate</h3>
                <p className="text-sm text-gray-600">BPM</p>
              </div>
            </div>
            {isConnected && metrics.heartRate > 0 && (
              <motion.div
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="w-3 h-3 bg-red-500 rounded-full"
              />
            )}
          </div>
          
          <div className={`p-3 rounded-lg ${getHealthStatus('heartRate', metrics.heartRate)}`}>
            <div className="text-2xl font-bold">
              {isConnected ? metrics.heartRate || "--" : "--"}
            </div>
            <div className="text-xs mt-1">
              {metrics.heartRate < 60 ? "Low" : metrics.heartRate > 100 ? "High" : "Normal"}
            </div>
          </div>
        </motion.div>

        {/* Steps Today */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Activity className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Steps Today</h3>
              <p className="text-sm text-gray-600">Total steps</p>
            </div>
          </div>
          
          <div className="p-3 rounded-lg bg-blue-50">
            <div className="text-2xl font-bold text-blue-900">
              {isConnected ? (metrics.stepsToday || 0).toLocaleString() : "--"}
            </div>
            <div className="text-xs mt-1 text-blue-700">
              Goal: 10,000 steps
            </div>
          </div>
        </motion.div>

        {/* Calories Burned */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Flame className="w-6 h-6 text-orange-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Calories Burned</h3>
              <p className="text-sm text-gray-600">kcal</p>
            </div>
          </div>
          
          <div className="p-3 rounded-lg bg-orange-50">
            <div className="text-2xl font-bold text-orange-900">
              {isConnected ? metrics.caloriesBurned || 0 : "--"}
            </div>
            <div className="text-xs mt-1 text-orange-700">
              Active burn
            </div>
          </div>
        </motion.div>

        {/* Blood Pressure */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Droplets className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Blood Pressure</h3>
              <p className="text-sm text-gray-600">mmHg</p>
            </div>
          </div>
          
          <div className="p-3 rounded-lg bg-purple-50">
            <div className="text-2xl font-bold text-purple-900">
              {isConnected && (metrics.bloodPressure.systolic || metrics.bloodPressure.diastolic) ? 
                `${metrics.bloodPressure.systolic}/${metrics.bloodPressure.diastolic}` : 
                "--/--"
              }
            </div>
            <div className="text-xs mt-1 text-purple-700">
              Systolic/Diastolic
            </div>
          </div>
        </motion.div>

        {/* Blood Oxygen Level */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-cyan-100 rounded-lg">
              <Wind className="w-6 h-6 text-cyan-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Blood Oxygen</h3>
              <p className="text-sm text-gray-600">SpO2</p>
            </div>
          </div>
          
          <div className={`p-3 rounded-lg ${getHealthStatus('bloodOxygenLevel', metrics.bloodOxygenLevel)}`}>
            <div className="text-2xl font-bold">
              {isConnected ? `${metrics.bloodOxygenLevel || 0}%` : "--%"}
            </div>
            <div className="text-xs mt-1">
              {metrics.bloodOxygenLevel < 95 ? "Low" : "Normal"}
            </div>
          </div>
        </motion.div>

        {/* Stress Level */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Activity className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Stress Level</h3>
              <p className="text-sm text-gray-600">0-10 scale</p>
            </div>
          </div>
          
          <div className={`p-3 rounded-lg ${getHealthStatus('stressLevel', metrics.stressLevel)}`}>
            <div className="text-2xl font-bold">
              {isConnected ? metrics.stressLevel || 0 : "--"}
            </div>
            <div className="text-xs mt-1">
              {metrics.stressLevel > 7 ? "High" : metrics.stressLevel > 4 ? "Medium" : "Low"}
            </div>
          </div>
        </motion.div>

        {/* Body Temperature */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.7 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-green-100 rounded-lg">
              <Thermometer className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Body Temperature</h3>
              <p className="text-sm text-gray-600">°F</p>
            </div>
          </div>
          
          <div className={`p-3 rounded-lg ${getHealthStatus('bodyTemperature', metrics.bodyTemperature)}`}>
            <div className="text-2xl font-bold">
              {isConnected ? `${metrics.bodyTemperature || 0}°` : "--°"}
            </div>
            <div className="text-xs mt-1">
              {metrics.bodyTemperature > 99.5 || metrics.bodyTemperature < 97 ? "Abnormal" : "Normal"}
            </div>
          </div>
        </motion.div>

        {/* Connection Info */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-gray-100 rounded-lg">
              <Watch className="w-6 h-6 text-gray-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Connection Status</h3>
              <p className="text-sm text-gray-600">SmartWatch Link</p>
            </div>
          </div>
          
          <div className="space-y-2">
            <div className={`p-2 rounded text-center text-sm font-medium ${getStatusColor()}`}>
              {isConnecting ? "Connecting..." : isConnected ? "Live Data" : "No Connection"}
            </div>
            {lastUpdate && (
              <div className="text-xs text-gray-500 text-center">
                Updated: {lastUpdate.toLocaleString()}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};