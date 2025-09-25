import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronLeft,
  ChevronRight,
  Heart,
  Scale,
  Ruler,
  Droplets,
  Target,
  Phone,
  CheckCircle,
  Activity,
  Skip,
  X,
  Plus,
  AlertTriangle,
  Pill,
  ShieldAlert,
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

export const HealthProfileFlow: React.FC<HealthProfileFlowProps> = ({
  onComplete,
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showCompletion, setShowCompletion] = useState(false);
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

  const steps = [
    {
      id: "height_cm",
      title: "What's your height?",
      subtitle: "Help us calculate your health metrics",
      icon: <Ruler className="w-8 h-8 text-[#76B3A8]" />,
      type: "number",
      placeholder: "Enter height in cm",
      suffix: "cm",
    },
    {
      id: "weight_kg",
      title: "What's your current weight?",
      subtitle: "This helps us track your progress",
      icon: <Scale className="w-8 h-8 text-[#76B3A8]" />,
      type: "number",
      placeholder: "Enter weight in kg",
      suffix: "kg",
    },
    {
      id: "activity_level",
      title: "What's your activity level?",
      subtitle: "This helps us calculate your caloric needs",
      icon: <Activity className="w-8 h-8 text-[#76B3A8]" />,
      type: "activity-select",
      options: activityLevelOptions,
    },
    {
      id: "blood_group",
      title: "What's your blood group?",
      subtitle: "Important for medical emergencies",
      icon: <Droplets className="w-8 h-8 text-[#76B3A8]" />,
      type: "select",
      options: bloodGroupOptions,
    },
    {
      id: "chronic_conditions",
      title: "Do you have any chronic conditions?",
      subtitle: "List any ongoing health conditions (comma separated)",
      icon: <Heart className="w-8 h-8 text-[#76B3A8]" />,
      type: "multi-text",
      placeholder: "e.g., diabetes, hypertension, asthma",
    },
    {
      id: "allergies",
      title: "Do you have any allergies?",
      subtitle: "List any known allergies (comma separated)",
      icon: <Heart className="w-8 h-8 text-[#76B3A8]" />,
      type: "multi-text",
      placeholder: "e.g., peanuts, shellfish, pollen",
    },
    {
      id: "current_medications",
      title: "Are you taking any medications?",
      subtitle: "List current medications (comma separated)",
      icon: <Heart className="w-8 h-8 text-[#76B3A8]" />,
      type: "multi-text",
      placeholder: "e.g., metformin, lisinopril, vitamin D",
    },
    {
      id: "daily_calorie_goal",
      title: "What's your daily calorie goal?",
      subtitle: "Target calories per day",
      icon: <Target className="w-8 h-8 text-[#76B3A8]" />,
      type: "number",
      placeholder: "Enter daily calorie goal",
      suffix: "calories",
    },
    {
      id: "daily_protein_goal",
      title: "What's your daily protein goal?",
      subtitle: "Target protein intake per day",
      icon: <Target className="w-8 h-8 text-[#76B3A8]" />,
      type: "number",
      placeholder: "Enter daily protein goal",
      suffix: "grams",
    },
    {
      id: "emergency_contact_name",
      title: "Emergency contact name",
      subtitle: "Who should we contact in case of emergency?",
      icon: <Phone className="w-8 h-8 text-[#76B3A8]" />,
      type: "text",
      placeholder: "Full name",
    },
    {
      id: "emergency_contact_relationship",
      title: "Relationship to emergency contact",
      subtitle: "How are they related to you?",
      icon: <Phone className="w-8 h-8 text-[#76B3A8]" />,
      type: "text",
      placeholder: "e.g., Spouse, Parent, Sibling, Friend",
    },
    {
      id: "emergency_contact_phone",
      title: "Emergency contact phone number",
      subtitle: "Their phone number",
      icon: <Phone className="w-8 h-8 text-[#76B3A8]" />,
      type: "tel",
      placeholder: "Phone number",
    },
  ];

  const handleInputChange = (
    stepId: string,
    value: string | number | string[]
  ) => {
    if (stepId.startsWith("emergency_contact_")) {
      const contactField = stepId.replace("emergency_contact_", "");
      setHealthProfile({
        ...healthProfile,
        emergency_contact: {
          ...healthProfile.emergency_contact,
          [contactField]: value,
        },
      });
    } else if (
      stepId === "chronic_conditions" ||
      stepId === "allergies" ||
      stepId === "current_medications"
    ) {
      const arrayValue =
        typeof value === "string"
          ? value
              .split(",")
              .map((item) => item.trim())
              .filter((item) => item.length > 0)
          : (value as string[]);
      setHealthProfile({
        ...healthProfile,
        [stepId]: arrayValue,
      });
    } else {
      setHealthProfile({
        ...healthProfile,
        [stepId]: value,
      });
    }
  };

  const getCurrentValue = (stepId: string): string | number => {
    if (stepId.startsWith("emergency_contact_")) {
      const contactField = stepId.replace("emergency_contact_", "");
      return (
        healthProfile.emergency_contact[
          contactField as keyof typeof healthProfile.emergency_contact
        ] || ""
      );
    } else if (
      stepId === "chronic_conditions" ||
      stepId === "allergies" ||
      stepId === "current_medications"
    ) {
      return healthProfile[stepId].join(", ");
    }
    return (
      (healthProfile[stepId as keyof HealthProfile] as string | number) || ""
    );
  };

  const isStepValid = (): boolean => {
    const currentStepData = steps[currentStep];
    const currentValue = getCurrentValue(currentStepData.id);

    // Optional fields (can be empty)
    if (
      ["chronic_conditions", "allergies", "current_medications"].includes(
        currentStepData.id
      )
    ) {
      return true;
    }

    // Required fields
    if (currentStepData.type === "number") {
      return Number(currentValue) > 0;
    }

    return currentValue !== "" && currentValue !== 0;
  };

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleSubmit();
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
      // Create a copy without activity_level for backend submission
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { activity_level, ...backendData } = healthProfile;
      await apiClient.storeHealthProfile({
        ...backendData,
        token,
      });
      setShowCompletion(true);
      setTimeout(() => {
        onComplete();
      }, 2000);
    } catch (error) {
      console.error("Failed to store health profile:", error);
      // Handle error - maybe show error message
    } finally {
      setIsSubmitting(false);
    }
  };

  if (showCompletion) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white to-gray-50 flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-6"
          >
            <CheckCircle className="w-10 h-10 text-green-600" />
          </motion.div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Health Profile Complete!
          </h1>
          <p className="text-xl text-gray-600">
            Taking you to your dashboard...
          </p>
        </motion.div>
      </div>
    );
  }

  const currentStepData = steps[currentStep];

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-gray-50 flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full"
      >
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <motion.div
              key={currentStep}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 200 }}
              className="inline-flex items-center justify-center w-16 h-16 bg-[#76B3A8]/10 rounded-full mb-4"
            >
              {currentStepData.icon}
            </motion.div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              {currentStepData.title}
            </h1>
            <p className="text-[#7D7F7C]">{currentStepData.subtitle}</p>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-[#7D7F7C]">Health Profile</span>
              <span className="text-sm text-[#7D7F7C]">
                {currentStep + 1} of {steps.length}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <motion.div
                className="bg-[#76B3A8] h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{
                  width: `${((currentStep + 1) / steps.length) * 100}%`,
                }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>

          {/* Input Field */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="mb-8"
            >
              {currentStepData.type === "select" ? (
                <div className="grid grid-cols-2 gap-3">
                  {currentStepData.options?.map((option) => (
                    <button
                      key={typeof option === "string" ? option : option.value}
                      onClick={() =>
                        handleInputChange(
                          currentStepData.id,
                          typeof option === "string" ? option : option.value
                        )
                      }
                      className={`p-4 rounded-lg border text-center transition-all duration-200 ${
                        getCurrentValue(currentStepData.id) ===
                        (typeof option === "string" ? option : option.value)
                          ? "bg-[#76B3A8] text-white border-[#76B3A8]"
                          : "bg-white text-gray-700 border-gray-300 hover:border-[#76B3A8]"
                      }`}
                    >
                      {typeof option === "string" ? option : option.label}
                    </button>
                  ))}
                </div>
              ) : currentStepData.type === "activity-select" ? (
                <div className="space-y-3">
                  {currentStepData.options?.map((option) => (
                    <button
                      key={typeof option === "string" ? option : option.value}
                      onClick={() =>
                        handleInputChange(
                          currentStepData.id,
                          typeof option === "string" ? option : option.value
                        )
                      }
                      className={`w-full p-4 rounded-lg border text-left transition-all duration-200 ${
                        getCurrentValue(currentStepData.id) ===
                        (typeof option === "string" ? option : option.value)
                          ? "bg-[#76B3A8] text-white border-[#76B3A8]"
                          : "bg-white text-gray-700 border-gray-300 hover:border-[#76B3A8]"
                      }`}
                    >
                      <div className="flex justify-between items-center">
                        <div>
                          <div className="font-semibold">
                            {typeof option === "string" ? option : option.label}
                          </div>
                          {typeof option !== "string" && option.description && (
                            <div className="text-sm opacity-75 mt-1">
                              {option.description}
                            </div>
                          )}
                        </div>
                        {getCurrentValue(currentStepData.id) ===
                          (typeof option === "string"
                            ? option
                            : option.value) && (
                          <div className="w-6 h-6 bg-white bg-opacity-30 rounded-full flex items-center justify-center">
                            <div className="w-2 h-2 bg-white rounded-full" />
                          </div>
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              ) : (
                <div className="relative">
                  {currentStepData.type === "multi-text" ? (
                    <textarea
                      value={getCurrentValue(currentStepData.id)}
                      onChange={(e) =>
                        handleInputChange(currentStepData.id, e.target.value)
                      }
                      placeholder={currentStepData.placeholder}
                      className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200 resize-none"
                      rows={3}
                    />
                  ) : (
                    <input
                      type={currentStepData.type}
                      value={getCurrentValue(currentStepData.id)}
                      onChange={(e) =>
                        handleInputChange(
                          currentStepData.id,
                          currentStepData.type === "number"
                            ? Number(e.target.value)
                            : e.target.value
                        )
                      }
                      placeholder={currentStepData.placeholder}
                      className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
                    />
                  )}
                  {currentStepData.suffix && (
                    <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500">
                      {currentStepData.suffix}
                    </span>
                  )}
                </div>
              )}
            </motion.div>
          </AnimatePresence>

          {/* Navigation Buttons */}
          <div className="flex justify-between">
            <button
              onClick={handleBack}
              disabled={currentStep === 0}
              className="flex items-center px-4 py-2 text-[#76B3A8] disabled:text-gray-400 disabled:cursor-not-allowed transition-colors duration-200"
            >
              <ChevronLeft className="w-4 h-4 mr-1" />
              Back
            </button>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleNext}
              disabled={isSubmitting || !isStepValid()}
              className="flex items-center px-6 py-3 bg-[#76B3A8] text-white rounded-lg font-semibold hover:bg-[#6BA399] transition-colors duration-200 disabled:opacity-50"
            >
              {isSubmitting
                ? "Saving..."
                : currentStep === steps.length - 1
                ? "Complete"
                : "Next"}
              {!isSubmitting && <ChevronRight className="w-4 h-4 ml-1" />}
            </motion.button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
