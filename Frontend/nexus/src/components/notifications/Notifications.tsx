import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bell,
  X,
  Calendar,
  Pill,
  AlertTriangle,
  Clock,
  Check,
  CheckCheck,
} from "lucide-react";

interface Notification {
  id: string;
  type: "appointment" | "medication" | "health_alert" | "reminder";
  title: string;
  message: string;
  timestamp: string;
  isRead: boolean;
  priority: "low" | "medium" | "high" | "critical";
  actionable?: boolean;
}

interface NotificationsProps {
  className?: string;
}

const mockNotifications: Notification[] = [
  {
    id: "1",
    type: "health_alert",
    title: "Critical Blood Pressure Reading",
    message: "Your blood pressure reading of 180/110 is critically high. Please contact your doctor immediately.",
    timestamp: "2025-09-25T10:30:00Z",
    isRead: false,
    priority: "critical",
    actionable: true,
  },
  {
    id: "2",
    type: "medication",
    title: "Medication Reminder",
    message: "Time to take your Lisinopril (10mg). Next dose in 24 hours.",
    timestamp: "2025-09-25T08:00:00Z",
    isRead: false,
    priority: "high",
    actionable: true,
  },
  {
    id: "3",
    type: "appointment",
    title: "Upcoming Appointment",
    message: "Appointment with Dr. Sarah Smith tomorrow at 2:00 PM. Remember to bring your lab results.",
    timestamp: "2025-09-24T16:00:00Z",
    isRead: true,
    priority: "medium",
    actionable: false,
  },
  {
    id: "4",
    type: "medication",
    title: "Low Medication Stock",
    message: "Your Metformin supply is running low (5 days remaining). Consider reordering soon.",
    timestamp: "2025-09-24T12:00:00Z",
    isRead: false,
    priority: "medium",
    actionable: true,
  },
  {
    id: "5",
    type: "reminder",
    title: "Health Check Reminder",
    message: "Don't forget to log your daily weight and water intake for today.",
    timestamp: "2025-09-24T07:00:00Z",
    isRead: true,
    priority: "low",
    actionable: false,
  },
  {
    id: "6",
    type: "health_alert",
    title: "Unusual Heart Rate Pattern",
    message: "Your heart rate has been elevated for the past 3 hours. Consider taking a break and relaxing.",
    timestamp: "2025-09-23T20:15:00Z",
    isRead: false,
    priority: "high",
    actionable: false,
  },
];

export const Notifications: React.FC<NotificationsProps> = ({ className = "" }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>(mockNotifications);
  const [filter, setFilter] = useState<"all" | "unread" | "critical">("all");
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const getNotificationIcon = (type: Notification["type"]) => {
    switch (type) {
      case "appointment":
        return <Calendar className="w-5 h-5" />;
      case "medication":
        return <Pill className="w-5 h-5" />;
      case "health_alert":
        return <AlertTriangle className="w-5 h-5" />;
      case "reminder":
        return <Clock className="w-5 h-5" />;
      default:
        return <Bell className="w-5 h-5" />;
    }
  };

  const getPriorityColor = (priority: Notification["priority"]) => {
    switch (priority) {
      case "critical":
        return "text-red-600 bg-red-50 border-red-200";
      case "high":
        return "text-orange-600 bg-orange-50 border-orange-200";
      case "medium":
        return "text-blue-600 bg-blue-50 border-blue-200";
      case "low":
        return "text-gray-600 bg-gray-50 border-gray-200";
      default:
        return "text-gray-600 bg-gray-50 border-gray-200";
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  const unreadCount = notifications.filter(n => !n.isRead).length;
  const criticalCount = notifications.filter(n => n.priority === "critical" && !n.isRead).length;

  const filteredNotifications = notifications.filter(notification => {
    switch (filter) {
      case "unread":
        return !notification.isRead;
      case "critical":
        return notification.priority === "critical";
      default:
        return true;
    }
  });

  const markAsRead = (id: string) => {
    setNotifications(prev =>
      prev.map(notification =>
        notification.id === id ? { ...notification, isRead: true } : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev =>
      prev.map(notification => ({ ...notification, isRead: true }))
    );
  };

  const dismissNotification = (id: string) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  };

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      {/* Bell Icon Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-gray-400 hover:text-gray-600 transition-colors"
        title="Notifications"
      >
        <Bell className="w-6 h-6" />
        
        {/* Badge */}
        {unreadCount > 0 && (
          <motion.span
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className={`absolute -top-1 -right-1 min-w-[20px] h-5 px-1 text-xs font-bold text-white rounded-full flex items-center justify-center ${
              criticalCount > 0 ? "bg-red-500" : "bg-[#76B3A8]"
            }`}
          >
            {unreadCount > 99 ? "99+" : unreadCount}
          </motion.span>
        )}
      </motion.button>

      {/* Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="absolute right-0 top-full mt-2 w-96 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 max-h-[600px] flex flex-col"
          >
            {/* Header */}
            <div className="p-4 border-b border-gray-100">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold text-gray-900">Notifications</h3>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              
              {/* Filters */}
              <div className="flex items-center space-x-2">
                <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
                  {["all", "unread", "critical"].map((filterOption) => (
                    <button
                      key={filterOption}
                      onClick={() => setFilter(filterOption as "all" | "unread" | "critical")}
                      className={`px-3 py-1 text-sm rounded-md transition-colors capitalize ${
                        filter === filterOption
                          ? "bg-white text-gray-900 shadow-sm"
                          : "text-gray-600 hover:text-gray-900"
                      }`}
                    >
                      {filterOption}
                    </button>
                  ))}
                </div>
                
                {unreadCount > 0 && (
                  <button
                    onClick={markAllAsRead}
                    className="flex items-center space-x-1 text-sm text-[#76B3A8] hover:text-[#6ba396] transition-colors"
                  >
                    <CheckCheck className="w-4 h-4" />
                    <span>Mark all read</span>
                  </button>
                )}
              </div>
            </div>

            {/* Notifications List */}
            <div className="flex-1 overflow-y-auto">
              {filteredNotifications.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-12 text-gray-500">
                  <Bell className="w-12 h-12 mb-3 text-gray-300" />
                  <p className="text-sm">No notifications</p>
                </div>
              ) : (
                <div className="divide-y divide-gray-100">
                  {filteredNotifications.map((notification) => (
                    <motion.div
                      key={notification.id}
                      layout
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      className={`p-4 hover:bg-gray-50 transition-colors ${
                        !notification.isRead ? "bg-blue-50/30" : ""
                      }`}
                    >
                      <div className="flex items-start space-x-3">
                        <div className={`p-2 rounded-lg border ${getPriorityColor(notification.priority)}`}>
                          {getNotificationIcon(notification.type)}
                        </div>
                        
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h4 className={`text-sm font-medium ${
                                !notification.isRead ? "text-gray-900" : "text-gray-700"
                              }`}>
                                {notification.title}
                              </h4>
                              <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                                {notification.message}
                              </p>
                              <div className="flex items-center space-x-3 mt-2">
                                <span className="text-xs text-gray-400">
                                  {formatTimestamp(notification.timestamp)}
                                </span>
                                {notification.priority === "critical" && (
                                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                                    Critical
                                  </span>
                                )}
                              </div>
                            </div>
                            
                            {/* Actions */}
                            <div className="flex items-center space-x-1 ml-2">
                              {!notification.isRead && (
                                <button
                                  onClick={() => markAsRead(notification.id)}
                                  className="p-1 text-gray-400 hover:text-[#76B3A8] transition-colors"
                                  title="Mark as read"
                                >
                                  <Check className="w-3 h-3" />
                                </button>
                              )}
                              <button
                                onClick={() => dismissNotification(notification.id)}
                                className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                                title="Dismiss"
                              >
                                <X className="w-3 h-3" />
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}
            </div>

            {/* Footer */}
            {filteredNotifications.length > 0 && (
              <div className="p-3 border-t border-gray-100">
                <button className="w-full text-sm text-[#76B3A8] hover:text-[#6ba396] transition-colors font-medium">
                  View All Notifications
                </button>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};