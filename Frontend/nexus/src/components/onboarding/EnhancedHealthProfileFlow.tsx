import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronLeft,
  ChevronRight,
  Scale,
  Ruler,
  Droplets,
  Target,
  Phone,
  CheckCircle,
  Activity,
  X,
  Plus,
  AlertTriangle,
  Pill,
  ShieldAlert,
  SkipForward,
} from "lucide-react";
import { HealthProfile } from "../../types";
import { apiClient } from "../../utils/api";

import Cookies from "js-cookie";

interface HealthProfileFlowProps {
  onComplete: () => void;
}

const bloodGroupOptions = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];

const activityLevelOptions = [
  {
    value: "sedentary",
    label: "Sedentary",
    description: "Little or no exercise",
  },
  {
    value: "light",
    label: "Light",
    description: "Light exercise 1-3 days/week",
  },
  {
    value: "moderate",
    label: "Moderate",
    description: "Moderate exercise 3-5 days/week",
  },
  {
    value: "active",
    label: "Active",
    description: "Heavy exercise 6-7 days/week",
  },
  {
    value: "very-active",
    label: "Very Active",
    description: "Very heavy exercise, physical job",
  },
];

const commonChronicConditions = [
  "Diabetes Type 1",
  "Diabetes Type 2",
  "Hypertension",
  "Heart Disease",
  "Asthma",
  "Arthritis",
  "Depression",
  "Anxiety",
  "Thyroid Disorders",
  "High Cholesterol",
];

const commonAllergies = [
  "Peanuts",
  "Tree Nuts",
  "Shellfish",
  "Fish",
  "Milk",
  "Eggs",
  "Soy",
  "Wheat/Gluten",
  "Pollen",
  "Dust Mites",
];

const commonMedications = [
  "Aspirin",
  "Ibuprofen",
  "Acetaminophen",
  "Metformin",
  "Lisinopril",
  "Atorvastatin",
  "Omeprazole",
  "Levothyroxine",
  "Multivitamin",
  "Fish Oil",
];

export const HealthProfileFlow: React.FC<HealthProfileFlowProps> = ({
  onComplete,
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showCompletion, setShowCompletion] = useState(false);
  const [heightUnit, setHeightUnit] = useState<"cm" | "inches">("cm");
  const [heightValue, setHeightValue] = useState("");

  const [customConditions, setCustomConditions] = useState("");
  const [customAllergies, setCustomAllergies] = useState("");
  const [customMedications, setCustomMedications] = useState("");

  const [healthProfile, setHealthProfile] = useState<HealthProfile>({
    height_cm: 0,
    weight_kg: 0,
    activity_level: "moderate",
    chronic_conditions: [],
    allergies: [],
    current_medications: [],
    blood_group: "",
    daily_calorie_goal: 0,
    daily_protein_goal: 0,
    emergency_contact: {
      name: "",
      relationship: "",
      phone: "",
    },
  });

  // Convert height from inches to cm
  const convertHeightToCm = (value: string, unit: "cm" | "inches"): number => {
    const numValue = parseFloat(value);
    if (isNaN(numValue)) return 0;
    return unit === "inches" ? Math.round(numValue * 2.54) : numValue;
  };

  const steps = [
    {
      id: "height_cm",
      title: "What's your height?",
      subtitle: "Help us calculate your health metrics accurately",
      icon: <Ruler className="w-8 h-8 text-[#76B3A8]" />,
      type: "height",
      canSkip: false,
    },
    {
      id: "weight_kg",
      title: "What's your current weight?",
      subtitle: "This helps us track your progress over time",
      icon: <Scale className="w-8 h-8 text-[#76B3A8]" />,
      type: "number",
      placeholder: "Enter weight in kg",
      suffix: "kg",
      canSkip: false,
    },
    {
      id: "activity_level",
      title: "What's your activity level?",
      subtitle: "This helps us calculate your daily caloric needs",
      icon: <Activity className="w-8 h-8 text-[#76B3A8]" />,
      type: "activity-select",
      canSkip: false,
    },
    {
      id: "blood_group",
      title: "What's your blood group?",
      subtitle: "Important for health tracking and emergencies",
      icon: <Droplets className="w-8 h-8 text-[#76B3A8]" />,
      type: "blood-select",
      canSkip: false,
    },
    {
      id: "chronic_conditions",
      title: "Do you have any chronic conditions?",
      subtitle: "Select any that apply to you (optional)",
      icon: <AlertTriangle className="w-8 h-8 text-orange-500" />,
      type: "chronic-conditions",
      canSkip: true,
    },
    {
      id: "allergies",
      title: "Do you have any allergies?",
      subtitle: "Help us provide safer food recommendations",
      icon: <ShieldAlert className="w-8 h-8 text-red-500" />,
      type: "allergies",
      canSkip: true,
    },
    {
      id: "current_medications",
      title: "Current medications or supplements?",
      subtitle: "This helps us avoid potential interactions",
      icon: <Pill className="w-8 h-8 text-blue-500" />,
      type: "medications",
      canSkip: true,
    },
    {
      id: "daily_calorie_goal",
      title: "Daily calorie goal",
      subtitle: "Based on your profile, we recommend this goal",
      icon: <Target className="w-8 h-8 text-[#76B3A8]" />,
      type: "number",
      placeholder: "Recommended: 2000",
      suffix: "kcal",
      canSkip: false,
    },
    {
      id: "daily_protein_goal",
      title: "Daily protein goal",
      subtitle: "Protein is essential for muscle maintenance",
      icon: <Target className="w-8 h-8 text-[#76B3A8]" />,
      type: "number",
      placeholder: "Recommended: 150",
      suffix: "grams",
      canSkip: false,
    },
    {
      id: "emergency_contact",
      title: "Emergency contact",
      subtitle: "Someone we can reach in case of emergency",
      icon: <Phone className="w-8 h-8 text-[#76B3A8]" />,
      type: "emergency-contact",
      canSkip: false,
    },
  ];

  const currentStepData = steps[currentStep];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleSubmit();
    }
  };

  const handleSkip = () => {
    if (currentStepData.canSkip) {
      handleNext();
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const token = Cookies.get("token");
      if (!token) {
        throw new Error("No authentication token found");
      }

      // Convert height to cm before submission
      const profileData = {
        ...healthProfile,
        height_cm: convertHeightToCm(heightValue, heightUnit),
      };

      // Remove the activity_level from the data sent to backend
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { activity_level, ...dataToSend } = profileData;

      await apiClient.storeHealthProfile({
        token,
        ...dataToSend,
      });

      setShowCompletion(true);
      setTimeout(() => {
        onComplete();
      }, 2000);
    } catch (error) {
      console.error("Failed to store health profile:", error);
      alert("Failed to save health profile. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleArraySelection = (
    field: "chronic_conditions" | "allergies" | "current_medications",
    value: string,
    customValue: string,
    setCustomValue: (value: string) => void
  ) => {
    const current = healthProfile[field] || [];
    let updated: string[];

    if (current.includes(value)) {
      updated = current.filter((item) => item !== value);
    } else {
      updated = [...current, value];
    }

    // Add custom values from text input
    if (customValue.trim()) {
      const customItems = customValue
        .split(",")
        .map((item) => item.trim())
        .filter((item) => item);
      updated = [...new Set([...updated, ...customItems])];
      setCustomValue("");
    }

    setHealthProfile((prev) => ({
      ...prev,
      [field]: updated,
    }));
  };

  const removeSelectedItem = (
    field: "chronic_conditions" | "allergies" | "current_medications",
    value: string
  ) => {
    const current = healthProfile[field] || [];
    const updated = current.filter((item) => item !== value);
    setHealthProfile((prev) => ({
      ...prev,
      [field]: updated,
    }));
  };

  const renderStepContent = () => {
    switch (currentStepData.type) {
      case "height":
        return (
          <div className="space-y-6">
            {/* Height Unit Selector */}
            <div className="flex justify-center space-x-4">
              <button
                onClick={() => setHeightUnit("cm")}
                className={`px-6 py-3 rounded-xl font-medium transition-all ${
                  heightUnit === "cm"
                    ? "bg-[#76B3A8] text-white shadow-lg"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                Centimeters (cm)
              </button>
              <button
                onClick={() => setHeightUnit("inches")}
                className={`px-6 py-3 rounded-xl font-medium transition-all ${
                  heightUnit === "inches"
                    ? "bg-[#76B3A8] text-white shadow-lg"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                Inches (in)
              </button>
            </div>

            {/* Height Input */}
            <div className="relative">
              <input
                type="number"
                value={heightValue}
                onChange={(e) => setHeightValue(e.target.value)}
                className="w-full px-4 py-4 text-xl border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-colors text-center"
                placeholder={
                  heightUnit === "cm"
                    ? "Enter height in cm (e.g., 175)"
                    : "Enter height in inches (e.g., 69)"
                }
              />
              <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 font-medium">
                {heightUnit}
              </span>
            </div>

            {heightValue && (
              <div className="text-center text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                {heightUnit === "inches" && (
                  <>
                    Converting to: {convertHeightToCm(heightValue, "inches")} cm
                  </>
                )}
                {heightUnit === "cm" && (
                  <>
                    That's approximately{" "}
                    {Math.round(parseFloat(heightValue) / 2.54)} inches
                  </>
                )}
              </div>
            )}
          </div>
        );

      case "chronic-conditions":
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-3">
              {commonChronicConditions.map((condition) => (
                <button
                  key={condition}
                  onClick={() =>
                    handleArraySelection(
                      "chronic_conditions",
                      condition,
                      customConditions,
                      setCustomConditions
                    )
                  }
                  className={`p-3 rounded-lg border-2 text-left transition-all ${
                    healthProfile.chronic_conditions?.includes(condition)
                      ? "border-orange-500 bg-orange-50 text-orange-800"
                      : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                  }`}
                >
                  <div className="font-medium text-sm">{condition}</div>
                </button>
              ))}
            </div>

            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-700">
                Other conditions (comma-separated):
              </label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={customConditions}
                  onChange={(e) => setCustomConditions(e.target.value)}
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                  placeholder="e.g., Fibromyalgia, Chronic fatigue"
                />
                <button
                  onClick={() =>
                    handleArraySelection(
                      "chronic_conditions",
                      "",
                      customConditions,
                      setCustomConditions
                    )
                  }
                  className="px-4 py-3 bg-[#76B3A8] text-white rounded-lg hover:bg-[#76B3A8]/80 transition-colors"
                >
                  <Plus className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Selected Items Display */}
            {healthProfile.chronic_conditions &&
              healthProfile.chronic_conditions.length > 0 && (
                <div className="space-y-2">
                  <p className="text-sm font-medium text-gray-700">
                    Selected conditions:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {healthProfile.chronic_conditions.map((condition) => (
                      <span
                        key={condition}
                        className="inline-flex items-center px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm"
                      >
                        {condition}
                        <button
                          onClick={() =>
                            removeSelectedItem("chronic_conditions", condition)
                          }
                          className="ml-2 hover:text-orange-600"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </span>
                    ))}
                  </div>
                </div>
              )}
          </div>
        );

      case "allergies":
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-3">
              {commonAllergies.map((allergy) => (
                <button
                  key={allergy}
                  onClick={() =>
                    handleArraySelection(
                      "allergies",
                      allergy,
                      customAllergies,
                      setCustomAllergies
                    )
                  }
                  className={`p-3 rounded-lg border-2 text-left transition-all ${
                    healthProfile.allergies?.includes(allergy)
                      ? "border-red-500 bg-red-50 text-red-800"
                      : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                  }`}
                >
                  <div className="font-medium text-sm">{allergy}</div>
                </button>
              ))}
            </div>

            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-700">
                Other allergies (comma-separated):
              </label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={customAllergies}
                  onChange={(e) => setCustomAllergies(e.target.value)}
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                  placeholder="e.g., Latex, Penicillin"
                />
                <button
                  onClick={() =>
                    handleArraySelection(
                      "allergies",
                      "",
                      customAllergies,
                      setCustomAllergies
                    )
                  }
                  className="px-4 py-3 bg-[#76B3A8] text-white rounded-lg hover:bg-[#76B3A8]/80 transition-colors"
                >
                  <Plus className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Selected Items Display */}
            {healthProfile.allergies && healthProfile.allergies.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm font-medium text-gray-700">
                  Selected allergies:
                </p>
                <div className="flex flex-wrap gap-2">
                  {healthProfile.allergies.map((allergy) => (
                    <span
                      key={allergy}
                      className="inline-flex items-center px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm"
                    >
                      {allergy}
                      <button
                        onClick={() => removeSelectedItem("allergies", allergy)}
                        className="ml-2 hover:text-red-600"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        );

      case "medications":
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-3">
              {commonMedications.map((medication) => (
                <button
                  key={medication}
                  onClick={() =>
                    handleArraySelection(
                      "current_medications",
                      medication,
                      customMedications,
                      setCustomMedications
                    )
                  }
                  className={`p-3 rounded-lg border-2 text-left transition-all ${
                    healthProfile.current_medications?.includes(medication)
                      ? "border-blue-500 bg-blue-50 text-blue-800"
                      : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                  }`}
                >
                  <div className="font-medium text-sm">{medication}</div>
                </button>
              ))}
            </div>

            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-700">
                Other medications/supplements (comma-separated):
              </label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={customMedications}
                  onChange={(e) => setCustomMedications(e.target.value)}
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                  placeholder="e.g., Metformin, Vitamin D"
                />
                <button
                  onClick={() =>
                    handleArraySelection(
                      "current_medications",
                      "",
                      customMedications,
                      setCustomMedications
                    )
                  }
                  className="px-4 py-3 bg-[#76B3A8] text-white rounded-lg hover:bg-[#76B3A8]/80 transition-colors"
                >
                  <Plus className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Selected Items Display */}
            {healthProfile.current_medications &&
              healthProfile.current_medications.length > 0 && (
                <div className="space-y-2">
                  <p className="text-sm font-medium text-gray-700">
                    Current medications/supplements:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {healthProfile.current_medications.map((medication) => (
                      <span
                        key={medication}
                        className="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                      >
                        {medication}
                        <button
                          onClick={() =>
                            removeSelectedItem(
                              "current_medications",
                              medication
                            )
                          }
                          className="ml-2 hover:text-blue-600"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </span>
                    ))}
                  </div>
                </div>
              )}
          </div>
        );

      case "activity-select":
        return (
          <div className="space-y-4">
            {activityLevelOptions.map((option) => (
              <motion.button
                key={option.value}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() =>
                  setHealthProfile((prev) => ({
                    ...prev,
                    activity_level: option.value as
                      | "sedentary"
                      | "light"
                      | "moderate"
                      | "active"
                      | "very-active",
                  }))
                }
                className={`w-full p-4 rounded-xl border-2 text-left transition-all ${
                  healthProfile.activity_level === option.value
                    ? "border-[#76B3A8] bg-[#76B3A8]/10"
                    : "border-gray-200 hover:border-gray-300"
                }`}
              >
                <div className="font-semibold text-gray-900">
                  {option.label}
                </div>
                <div className="text-sm text-gray-600">
                  {option.description}
                </div>
              </motion.button>
            ))}
          </div>
        );

      case "blood-select":
        return (
          <div className="grid grid-cols-4 gap-3">
            {bloodGroupOptions.map((group) => (
              <motion.button
                key={group}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() =>
                  setHealthProfile((prev) => ({ ...prev, blood_group: group }))
                }
                className={`p-4 rounded-xl border-2 font-semibold transition-all ${
                  healthProfile.blood_group === group
                    ? "border-[#76B3A8] bg-[#76B3A8]/10 text-[#76B3A8]"
                    : "border-gray-200 hover:border-gray-300 text-gray-700"
                }`}
              >
                {group}
              </motion.button>
            ))}
          </div>
        );

      case "number":
        return (
          <div className="relative">
            <input
              type="number"
              value={
                (healthProfile[
                  currentStepData.id as keyof HealthProfile
                ] as number) || ""
              }
              onChange={(e) =>
                setHealthProfile((prev) => ({
                  ...prev,
                  [currentStepData.id]: parseFloat(e.target.value) || 0,
                }))
              }
              className="w-full px-4 py-4 text-xl border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-colors text-center"
              placeholder={currentStepData.placeholder}
            />
            {currentStepData.suffix && (
              <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 font-medium">
                {currentStepData.suffix}
              </span>
            )}
          </div>
        );

      case "emergency-contact":
        return (
          <div className="space-y-4">
            <input
              type="text"
              value={healthProfile.emergency_contact.name}
              onChange={(e) =>
                setHealthProfile((prev) => ({
                  ...prev,
                  emergency_contact: {
                    ...prev.emergency_contact,
                    name: e.target.value,
                  },
                }))
              }
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-colors"
              placeholder="Full name"
            />
            <input
              type="text"
              value={healthProfile.emergency_contact.relationship}
              onChange={(e) =>
                setHealthProfile((prev) => ({
                  ...prev,
                  emergency_contact: {
                    ...prev.emergency_contact,
                    relationship: e.target.value,
                  },
                }))
              }
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-colors"
              placeholder="Relationship (e.g., Spouse, Parent)"
            />
            <input
              type="tel"
              value={healthProfile.emergency_contact.phone}
              onChange={(e) =>
                setHealthProfile((prev) => ({
                  ...prev,
                  emergency_contact: {
                    ...prev.emergency_contact,
                    phone: e.target.value,
                  },
                }))
              }
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-colors"
              placeholder="Phone number"
            />
          </div>
        );

      default:
        return null;
    }
  };

  if (showCompletion) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center py-12"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <CheckCircle className="w-24 h-24 text-green-500 mx-auto mb-6" />
        </motion.div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Health Profile Complete!
        </h2>
        <p className="text-gray-600 text-lg">
          Your personalized health journey begins now.
        </p>
      </motion.div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <span className="text-sm font-medium text-gray-600">
            Step {currentStep + 1} of {steps.length}
          </span>
          <span className="text-sm font-medium text-[#76B3A8]">
            {Math.round(((currentStep + 1) / steps.length) * 100)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className="bg-[#76B3A8] h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{
              width: `${((currentStep + 1) / steps.length) * 100}%`,
            }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          transition={{ duration: 0.3 }}
          className="bg-white rounded-2xl shadow-lg p-8"
        >
          {/* Step Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-[#76B3A8]/10 rounded-full mb-4">
              {currentStepData.icon}
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {currentStepData.title}
            </h2>
            <p className="text-gray-600">{currentStepData.subtitle}</p>
          </div>

          {/* Step Content */}
          <div className="mb-8">{renderStepContent()}</div>

          {/* Navigation Buttons */}
          <div className="flex justify-between items-center">
            <button
              onClick={handleBack}
              disabled={currentStep === 0}
              className={`flex items-center px-6 py-3 rounded-xl font-medium transition-colors ${
                currentStep === 0
                  ? "text-gray-400 cursor-not-allowed"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              <ChevronLeft className="w-5 h-5 mr-2" />
              Back
            </button>

            <div className="flex space-x-3">
              {currentStepData.canSkip && (
                <button
                  onClick={handleSkip}
                  className="flex items-center px-6 py-3 text-gray-600 hover:bg-gray-100 rounded-xl font-medium transition-colors"
                >
                  <SkipForward className="w-5 h-5 mr-2" />
                  Skip
                </button>
              )}

              <button
                onClick={handleNext}
                disabled={isSubmitting}
                className="flex items-center px-8 py-3 bg-[#76B3A8] text-white rounded-xl font-medium hover:bg-[#76B3A8]/80 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{
                      duration: 1,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                    className="w-5 h-5 border-2 border-white border-t-transparent rounded-full mr-2"
                  />
                ) : currentStep === steps.length - 1 ? (
                  <>
                    <CheckCircle className="w-5 h-5 mr-2" />
                    Complete
                  </>
                ) : (
                  <>
                    Next
                    <ChevronRight className="w-5 h-5 ml-2" />
                  </>
                )}
              </button>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};
