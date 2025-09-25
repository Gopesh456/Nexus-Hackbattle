import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Heart, 
  Activity, 
  Droplets, 
  Moon, 
  Target, 
  TrendingUp,
  Calendar,
  Plus,
  Settings,
  LogOut
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useAuth } from '../contexts/AuthContext';
import { HealthMetrics } from '../types';

const mockHealthData = [
  { date: '2025-01-01', weight: 180, steps: 8500, water: 64, sleep: 7.5 },
  { date: '2025-01-02', weight: 179.5, steps: 9200, water: 72, sleep: 8.0 },
  { date: '2025-01-03', weight: 179.2, steps: 7800, water: 56, sleep: 6.5 },
  { date: '2025-01-04', weight: 178.8, steps: 10500, water: 80, sleep: 7.8 },
  { date: '2025-01-05', weight: 178.5, steps: 9800, water: 68, sleep: 7.2 },
  { date: '2025-01-06', weight: 178.2, steps: 11200, water: 76, sleep: 8.5 },
  { date: '2025-01-07', weight: 177.9, steps: 9600, water: 64, sleep: 7.9 },
];

const mockMetrics: HealthMetrics = {
  weight: 177.9,
  steps: 9600,
  waterIntake: 64,
  sleep: 7.9,
  heartRate: 72,
  caloriesBurned: 2340,
};

export const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [selectedMetric, setSelectedMetric] = useState('weight');

  const metricCards = [
    {
      id: 'weight',
      title: 'Weight',
      value: `${mockMetrics.weight} lbs`,
      change: '-0.3 lbs',
      icon: Target,
      color: '#76B3A8',
      bgColor: 'bg-[#76B3A8]/10',
    },
    {
      id: 'steps',
      title: 'Steps',
      value: mockMetrics.steps.toLocaleString(),
      change: '+1,200',
      icon: Activity,
      color: '#3B82F6',
      bgColor: 'bg-blue-50',
    },
    {
      id: 'water',
      title: 'Water Intake',
      value: `${mockMetrics.waterIntake} oz`,
      change: '+8 oz',
      icon: Droplets,
      color: '#06B6D4',
      bgColor: 'bg-cyan-50',
    },
    {
      id: 'sleep',
      title: 'Sleep',
      value: `${mockMetrics.sleep}h`,
      change: '+0.7h',
      icon: Moon,
      color: '#8B5CF6',
      bgColor: 'bg-purple-50',
    },
    {
      id: 'heartRate',
      title: 'Heart Rate',
      value: `${mockMetrics.heartRate} bpm`,
      change: '-2 bpm',
      icon: Heart,
      color: '#EF4444',
      bgColor: 'bg-red-50',
    },
    {
      id: 'calories',
      title: 'Calories Burned',
      value: mockMetrics.caloriesBurned.toLocaleString(),
      change: '+340',
      icon: TrendingUp,
      color: '#F59E0B',
      bgColor: 'bg-amber-50',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-[#76B3A8] rounded-full flex items-center justify-center">
                <Heart className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">HealthApp</h1>
                <p className="text-sm text-[#7D7F7C]">Welcome back, {user?.user}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-[#7D7F7C] hover:text-gray-900 transition-colors duration-200"
              >
                <Settings className="w-5 h-5" />
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={logout}
                className="p-2 text-[#7D7F7C] hover:text-red-500 transition-colors duration-200"
              >
                <LogOut className="w-5 h-5" />
              </motion.button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Actions */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Today's Overview</h2>
            <div className="flex items-center space-x-2">
              <Calendar className="w-4 h-4 text-[#7D7F7C]" />
              <span className="text-sm text-[#7D7F7C]">
                {new Date().toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </span>
            </div>
          </div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {metricCards.map((card, index) => {
              const IconComponent = card.icon;
              return (
                <motion.div
                  key={card.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => setSelectedMetric(card.id)}
                  className={`${card.bgColor} rounded-2xl p-6 cursor-pointer transition-all duration-200 border-2 ${
                    selectedMetric === card.id ? 'border-[#76B3A8]' : 'border-transparent'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-[#7D7F7C] text-sm font-medium mb-1">{card.title}</p>
                      <p className="text-2xl font-bold text-gray-900 mb-1">{card.value}</p>
                      <div className="flex items-center">
                        <span className="text-green-600 text-sm font-medium">{card.change}</span>
                        <span className="text-[#7D7F7C] text-xs ml-1">vs yesterday</span>
                      </div>
                    </div>
                    <div 
                      className="w-12 h-12 rounded-xl flex items-center justify-center"
                      style={{ backgroundColor: card.color }}
                    >
                      <IconComponent className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Chart Section */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-900">Progress Chart</h3>
            <select 
              value={selectedMetric}
              onChange={(e) => setSelectedMetric(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
            >
              {metricCards.map(metric => (
                <option key={metric.id} value={metric.id}>
                  {metric.title}
                </option>
              ))}
            </select>
          </div>

          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockHealthData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={(date) => new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  stroke="#7D7F7C"
                />
                <YAxis stroke="#7D7F7C" />
                <Tooltip 
                  labelFormatter={(date) => new Date(date).toLocaleDateString()}
                  contentStyle={{
                    backgroundColor: 'white',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey={selectedMetric}
                  stroke="#76B3A8" 
                  strokeWidth={3}
                  dot={{ fill: '#76B3A8', strokeWidth: 2, r: 6 }}
                  activeDot={{ r: 8, fill: '#76B3A8' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Quick Add Section */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Quick Actions</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center justify-center p-6 border-2 border-dashed border-[#76B3A8] rounded-xl text-[#76B3A8] hover:bg-[#76B3A8]/5 transition-colors duration-200"
            >
              <Plus className="w-6 h-6 mr-3" />
              Log Food
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center justify-center p-6 border-2 border-dashed border-[#76B3A8] rounded-xl text-[#76B3A8] hover:bg-[#76B3A8]/5 transition-colors duration-200"
            >
              <Plus className="w-6 h-6 mr-3" />
              Add Exercise
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center justify-center p-6 border-2 border-dashed border-[#76B3A8] rounded-xl text-[#76B3A8] hover:bg-[#76B3A8]/5 transition-colors duration-200"
            >
              <Plus className="w-6 h-6 mr-3" />
              Update Weight
            </motion.button>
          </div>
        </div>
      </div>
    </div>
  );
};