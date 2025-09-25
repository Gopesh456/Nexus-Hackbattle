import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { PersonalInfoStep } from './PersonalInfoStep';
import { ActivityLevelStep } from './ActivityLevelStep';
import { GoalsStep } from './GoalsStep';
import { MedicalHistoryStep } from './MedicalHistoryStep';
import { HealthProfile } from '../../types';

interface OnboardingFlowProps {
  onComplete: (profile: HealthProfile) => void;
}

export const OnboardingFlow: React.FC<OnboardingFlowProps> = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [profile, setProfile] = useState<Partial<HealthProfile>>({});

  const steps = [
    { component: PersonalInfoStep, title: 'Personal Information' },
    { component: ActivityLevelStep, title: 'Activity Level' },
    { component: GoalsStep, title: 'Health Goals' },
    { component: MedicalHistoryStep, title: 'Medical History' },
  ];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onComplete(profile as HealthProfile);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const updateProfile = (data: Partial<HealthProfile>) => {
    setProfile({ ...profile, ...data });
  };

  const CurrentStepComponent = steps[currentStep].component;

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-gray-50 px-4 py-8">
      <div className="max-w-2xl mx-auto">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-[#7D7F7C]">
              Step {currentStep + 1} of {steps.length}
            </span>
            <span className="text-sm text-[#7D7F7C]">
              {Math.round(((currentStep + 1) / steps.length) * 100)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
              transition={{ duration: 0.5 }}
              className="bg-[#76B3A8] h-2 rounded-full"
            />
          </div>
        </div>

        {/* Step Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
            className="bg-white rounded-2xl shadow-xl p-8 mb-8"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              {steps[currentStep].title}
            </h2>
            <CurrentStepComponent
              data={profile}
              onUpdate={updateProfile}
            />
          </motion.div>
        </AnimatePresence>

        {/* Navigation */}
        <div className="flex justify-between">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleBack}
            disabled={currentStep === 0}
            className="flex items-center px-6 py-3 text-[#7D7F7C] disabled:opacity-50 disabled:cursor-not-allowed hover:text-gray-900 transition-colors duration-200"
          >
            <ChevronLeft className="w-5 h-5 mr-2" />
            Back
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleNext}
            className="flex items-center px-6 py-3 bg-[#76B3A8] text-white rounded-lg font-semibold hover:bg-[#6BA399] transition-colors duration-200"
          >
            {currentStep === steps.length - 1 ? 'Complete' : 'Next'}
            {currentStep < steps.length - 1 && (
              <ChevronRight className="w-5 h-5 ml-2" />
            )}
          </motion.button>
        </div>
      </div>
    </div>
  );
};