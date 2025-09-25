import React from "react";
import { motion } from "framer-motion";
import {
  Home,
  Utensils,
  Bot,
  FlaskConical,
  LogOut,
  User,
  Settings,
} from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";
import { Notifications } from "../notifications/Notifications";

interface SidebarProps {
  activePage: string;
  onPageChange: (page: string) => void;
}

const navigationItems = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: Home,
    color: "text-blue-600",
    bgColor: "bg-blue-50",
  },
  {
    id: "food-diary",
    label: "Food Diary",
    icon: Utensils,
    color: "text-green-600",
    bgColor: "bg-green-50",
  },
  {
    id: "nurse-agent",
    label: "Nurse Agent",
    icon: Bot,
    color: "text-purple-600",
    bgColor: "bg-purple-50",
  },
  {
    id: "lab-medications",
    label: "Labs & Medications",
    icon: FlaskConical,
    color: "text-orange-600",
    bgColor: "bg-orange-50",
  },
  {
    id: "profile",
    label: "Profile",
    icon: User,
    color: "text-indigo-600",
    bgColor: "bg-indigo-50",
  },
];

export const Sidebar: React.FC<SidebarProps> = ({
  activePage,
  onPageChange,
}) => {
  const { user, logout } = useAuth();

  return (
    <div className="h-screen w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-[#76B3A8] to-[#5A9B8E] rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-lg">N</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Nexus</h1>
              <p className="text-sm text-gray-500">Health Platform</p>
            </div>
          </div>

          {/* Notifications */}
          <Notifications />
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6">
        <div className="space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.id;

            return (
              <motion.button
                key={item.id}
                onClick={() => onPageChange(item.id)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-left transition-all duration-200 ${
                  isActive
                    ? `${item.bgColor} ${item.color} font-medium`
                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                }`}
              >
                <Icon
                  className={`w-5 h-5 ${
                    isActive ? item.color : "text-gray-400"
                  }`}
                />
                <span>{item.label}</span>
              </motion.button>
            );
          })}
        </div>
      </nav>

      {/* User Profile & Logout */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
            <User className="w-4 h-4 text-gray-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">
              {user?.user || "User"}
            </p>
            <p className="text-xs text-gray-500">Health Member</p>
          </div>
        </div>

        <motion.button
          onClick={logout}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full flex items-center space-x-3 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-all duration-200"
        >
          <LogOut className="w-4 h-4" />
          <span className="text-sm">Logout</span>
        </motion.button>
      </div>
    </div>
  );
};
