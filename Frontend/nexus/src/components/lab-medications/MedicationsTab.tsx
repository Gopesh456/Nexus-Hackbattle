import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Pill,
  Clock,
  Edit3,
  Trash2,
  Calendar,
  ShoppingCart,
  Bell,
  Zap,
  Plus,
  X,
  Save,
  AlertCircle,
} from "lucide-react";

interface Medication {
  id: string;
  medName: string;
  numberOfPills: number;
  frequencyPerDay: number;
  medicalCondition: string;
  nextOrderDate: string;
  everydayReminder: boolean;
  reminderTime: string;
  autoOrdering: boolean;
}

interface EditingMedication extends Partial<Medication> {
  id?: string;
}

export const MedicationsTab: React.FC = () => {
  const [medications, setMedications] = useState<Medication[]>([
    {
      id: "1",
      medName: "Lisinopril",
      numberOfPills: 30,
      frequencyPerDay: 1,
      medicalCondition: "High Blood Pressure",
      nextOrderDate: "2025-10-15",
      everydayReminder: true,
      reminderTime: "08:00",
      autoOrdering: true,
    },
    {
      id: "2",
      medName: "Metformin",
      numberOfPills: 60,
      frequencyPerDay: 2,
      medicalCondition: "Type 2 Diabetes",
      nextOrderDate: "2025-10-20",
      everydayReminder: true,
      reminderTime: "08:00",
      autoOrdering: false,
    },
    {
      id: "3",
      medName: "Vitamin D3",
      numberOfPills: 90,
      frequencyPerDay: 1,
      medicalCondition: "Vitamin D Deficiency",
      nextOrderDate: "2025-11-01",
      everydayReminder: false,
      reminderTime: "09:00",
      autoOrdering: true,
    },
    {
      id: "4",
      medName: "Atorvastatin",
      numberOfPills: 30,
      frequencyPerDay: 1,
      medicalCondition: "High Cholesterol",
      nextOrderDate: "2025-10-25",
      everydayReminder: true,
      reminderTime: "21:00",
      autoOrdering: false,
    },
  ]);

  const [editingMed, setEditingMed] = useState<EditingMedication | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const getDaysUntilNextOrder = (nextOrderDate: string) => {
    const today = new Date();
    const orderDate = new Date(nextOrderDate);
    const timeDiff = orderDate.getTime() - today.getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
    return daysDiff;
  };

  const handleEdit = (medication: Medication) => {
    setEditingMed({ ...medication });
  };

  const handleSave = () => {
    if (!editingMed) return;

    if (editingMed.id) {
      // Update existing medication
      setMedications((prev) =>
        prev.map((med) =>
          med.id === editingMed.id
            ? ({ ...med, ...editingMed } as Medication)
            : med
        )
      );
    } else {
      // Add new medication
      const newMed: Medication = {
        ...editingMed,
        id: Date.now().toString(),
      } as Medication;
      setMedications((prev) => [...prev, newMed]);
    }

    setEditingMed(null);
    setShowAddForm(false);
  };

  const handleDelete = (id: string) => {
    setMedications((prev) => prev.filter((med) => med.id !== id));
  };

  const handleAddNew = () => {
    setEditingMed({
      medName: "",
      numberOfPills: 0,
      frequencyPerDay: 1,
      medicalCondition: "",
      nextOrderDate: new Date().toISOString().split("T")[0],
      everydayReminder: false,
      reminderTime: "08:00",
      autoOrdering: false,
    });
    setShowAddForm(true);
  };

  const handleOrderNow = (medication: Medication) => {
    // Simulate ordering logic
    alert(`Ordering ${medication.medName} now...`);
  };

  return (
    <div className="space-y-6">
      {/* Add Medication Button */}
      <div className="flex justify-end">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleAddNew}
          className="flex items-center space-x-2 bg-[#76B3A8] text-white px-4 py-2 rounded-lg hover:bg-[#6ba396] transition-all"
        >
          <Plus className="w-5 h-5" />
          <span>Add Medication</span>
        </motion.button>
      </div>

      {/* Medications Grid */}
      <div className="grid gap-6">
        {medications.map((medication, index) => (
          <motion.div
            key={medication.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden"
          >
            {/* Medication Header */}
            <div className="p-6 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-16 bg-gradient-to-r from-[#76B3A8] to-[#5A9B8E] rounded-xl flex items-center justify-center">
                    <Pill className="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">
                      {medication.medName}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {medication.medicalCondition}
                    </p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500 mt-2">
                      <span className="flex items-center space-x-1">
                        <Pill className="w-4 h-4" />
                        <span>{medication.numberOfPills} pills</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>{medication.frequencyPerDay}x daily</span>
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  {/* Auto Order Badge */}
                  {medication.autoOrdering && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="flex items-center space-x-1 bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium"
                    >
                      <Zap className="w-4 h-4" />
                      <span>Auto Order</span>
                    </motion.div>
                  )}

                  {/* Action Buttons */}
                  <div className="flex items-center space-x-1">
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => handleEdit(medication)}
                      className="p-2 text-gray-400 hover:text-[#76B3A8] transition-colors"
                      title="Edit medication"
                    >
                      <Edit3 className="w-5 h-5" />
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => handleDelete(medication.id)}
                      className="p-2 text-gray-400 hover:text-red-500 transition-colors"
                      title="Delete medication"
                    >
                      <Trash2 className="w-5 h-5" />
                    </motion.button>
                  </div>
                </div>
              </div>
            </div>

            {/* Medication Details */}
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Next Order & Reminder Info */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <Calendar className="w-5 h-5 text-blue-600" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          Next Order
                        </p>
                        <p className="text-sm text-gray-600">
                          {formatDate(medication.nextOrderDate)}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-500">
                        {getDaysUntilNextOrder(medication.nextOrderDate)} days
                      </p>
                    </div>
                  </div>

                  {medication.everydayReminder && (
                    <div className="flex items-center space-x-3 p-4 bg-yellow-50 rounded-lg">
                      <Bell className="w-5 h-5 text-yellow-600" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          Daily Reminder
                        </p>
                        <p className="text-sm text-gray-600">
                          Every day at {medication.reminderTime}
                        </p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Order Actions */}
                <div className="space-y-4">
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleOrderNow(medication)}
                    className="w-full flex items-center justify-center space-x-2 bg-[#76B3A8] text-white px-4 py-3 rounded-lg hover:bg-[#6ba396] transition-all"
                  >
                    <ShoppingCart className="w-5 h-5" />
                    <span>Order Now</span>
                  </motion.button>

                  {getDaysUntilNextOrder(medication.nextOrderDate) <= 7 && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex items-center space-x-2 p-3 bg-orange-50 border border-orange-200 rounded-lg"
                    >
                      <AlertCircle className="w-5 h-5 text-orange-600" />
                      <span className="text-sm text-orange-800">
                        Order soon - running low!
                      </span>
                    </motion.div>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Add/Edit Medication Modal */}
      <AnimatePresence>
        {(showAddForm || editingMed) && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            >
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-2xl font-bold text-gray-900">
                    {editingMed?.id ? "Edit Medication" : "Add New Medication"}
                  </h2>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => {
                      setEditingMed(null);
                      setShowAddForm(false);
                    }}
                    className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                  >
                    <X className="w-6 h-6" />
                  </motion.button>
                </div>
              </div>

              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Medicine Name *
                    </label>
                    <input
                      type="text"
                      value={editingMed?.medName || ""}
                      onChange={(e) =>
                        setEditingMed((prev) => ({
                          ...prev,
                          medName: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      placeholder="e.g., Lisinopril"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Number of Pills *
                    </label>
                    <input
                      type="number"
                      value={editingMed?.numberOfPills || ""}
                      onChange={(e) =>
                        setEditingMed((prev) => ({
                          ...prev,
                          numberOfPills: parseInt(e.target.value) || 0,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      placeholder="30"
                      min="1"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Frequency Per Day *
                    </label>
                    <select
                      value={editingMed?.frequencyPerDay || 1}
                      onChange={(e) =>
                        setEditingMed((prev) => ({
                          ...prev,
                          frequencyPerDay: parseInt(e.target.value),
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                    >
                      <option value={1}>Once daily</option>
                      <option value={2}>Twice daily</option>
                      <option value={3}>Three times daily</option>
                      <option value={4}>Four times daily</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Medical Condition *
                    </label>
                    <input
                      type="text"
                      value={editingMed?.medicalCondition || ""}
                      onChange={(e) =>
                        setEditingMed((prev) => ({
                          ...prev,
                          medicalCondition: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      placeholder="e.g., High Blood Pressure"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Next Order Date *
                    </label>
                    <input
                      type="date"
                      value={editingMed?.nextOrderDate || ""}
                      onChange={(e) =>
                        setEditingMed((prev) => ({
                          ...prev,
                          nextOrderDate: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Reminder Time
                    </label>
                    <input
                      type="time"
                      value={editingMed?.reminderTime || ""}
                      onChange={(e) =>
                        setEditingMed((prev) => ({
                          ...prev,
                          reminderTime: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      disabled={!editingMed?.everydayReminder}
                    />
                  </div>

                  <div className="md:col-span-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <label className="flex items-center space-x-3">
                          <input
                            type="checkbox"
                            checked={editingMed?.everydayReminder || false}
                            onChange={(e) =>
                              setEditingMed((prev) => ({
                                ...prev,
                                everydayReminder: e.target.checked,
                              }))
                            }
                            className="w-5 h-5 text-[#76B3A8] border-gray-300 rounded focus:ring-[#76B3A8]"
                          />
                          <span className="text-sm font-medium text-gray-700">
                            Enable daily reminder
                          </span>
                        </label>
                      </div>

                      <div className="flex items-center space-x-4">
                        <label className="flex items-center space-x-3">
                          <input
                            type="checkbox"
                            checked={editingMed?.autoOrdering || false}
                            onChange={(e) =>
                              setEditingMed((prev) => ({
                                ...prev,
                                autoOrdering: e.target.checked,
                              }))
                            }
                            className="w-5 h-5 text-[#76B3A8] border-gray-300 rounded focus:ring-[#76B3A8]"
                          />
                          <span className="text-sm font-medium text-gray-700">
                            Enable auto ordering
                          </span>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex space-x-3 mt-8">
                  <button
                    onClick={() => {
                      setEditingMed(null);
                      setShowAddForm(false);
                    }}
                    className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-all"
                  >
                    Cancel
                  </button>
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={handleSave}
                    className="flex-1 flex items-center justify-center space-x-2 bg-[#76B3A8] text-white px-6 py-3 rounded-lg hover:bg-[#6ba396] transition-all"
                  >
                    <Save className="w-5 h-5" />
                    <span>Save Medication</span>
                  </motion.button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
