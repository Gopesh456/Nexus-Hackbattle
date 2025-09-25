import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, User, Calendar, MapPin, Mail, Phone, Users, CheckCircle } from 'lucide-react';
import { BasicInfo } from '../../types';
import { apiClient } from '../../utils/api';
import Cookies from 'js-cookie';

interface BasicInfoFlowProps {
  onComplete: () => void;
}

const genderOptions = [
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'non-binary', label: 'Non-binary' },
  { value: 'prefer-not-to-say', label: 'Prefer not to say' },
];

const mockLocations = [
  'New York, NY',
  'Los Angeles, CA',
  'Chicago, IL',
  'Houston, TX',
  'Phoenix, AZ',
  'Philadelphia, PA',
  'San Antonio, TX',
  'San Diego, CA',
  'Dallas, TX',
  'San Jose, CA',
];

export const BasicInfoFlow: React.FC<BasicInfoFlowProps> = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showCompletion, setShowCompletion] = useState(false);
  const [locationSuggestions, setLocationSuggestions] = useState<string[]>([]);
  const [basicInfo, setBasicInfo] = useState<BasicInfo>({
    full_name: '',
    date_of_birth: '',
    gender: '',
    location: '',
    email: '',
    phone: '',
  });

  const steps = [
    {
      id: 'full_name',
      title: "What's your full name?",
      subtitle: 'We use this to personalize your experience',
      icon: User,
      type: 'text',
      placeholder: 'Enter your full name',
    },
    {
      id: 'date_of_birth',
      title: "When's your birthday?",
      subtitle: 'This helps us provide age-appropriate recommendations',
      icon: Calendar,
      type: 'date',
      placeholder: '',
    },
    {
      id: 'gender',
      title: 'How do you identify?',
      subtitle: 'This helps us customize your health insights',
      icon: Users,
      type: 'select',
      options: genderOptions,
    },
    {
      id: 'location',
      title: 'Where are you located?',
      subtitle: 'We can suggest local health resources and activities',
      icon: MapPin,
      type: 'autocomplete',
      placeholder: 'Start typing your city...',
    },
    {
      id: 'email',
      title: "What's your email?",
      subtitle: 'For important health updates and reminders',
      icon: Mail,
      type: 'email',
      placeholder: 'Enter your email address',
    },
    {
      id: 'phone',
      title: "What's your phone number?",
      subtitle: 'Optional - for appointment reminders and alerts',
      icon: Phone,
      type: 'tel',
      placeholder: 'Enter your phone number',
    },
  ];

  const handleNext = async () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      await handleSubmit();
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
      const token = Cookies.get('token');
      await apiClient.storeBasicInfo({
        token,
        ...basicInfo,
      });
      setShowCompletion(true);
      setTimeout(() => {
        onComplete();
      }, 3000);
    } catch (error) {
      console.error('Failed to store basic info:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const updateBasicInfo = (field: keyof BasicInfo, value: string) => {
    setBasicInfo({ ...basicInfo, [field]: value });
  };

  const handleLocationSearch = (value: string) => {
    updateBasicInfo('location', value);
    if (value.length > 1) {
      const filtered = mockLocations.filter(location =>
        location.toLowerCase().includes(value.toLowerCase())
      );
      setLocationSuggestions(filtered.slice(0, 5));
    } else {
      setLocationSuggestions([]);
    }
  };

  const isStepValid = () => {
    const currentField = steps[currentStep].id as keyof BasicInfo;
    const value = basicInfo[currentField];
    
    // Phone is optional
    if (currentField === 'phone') return true;
    
    return value && value.trim().length > 0;
  };

  if (showCompletion) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white to-gray-50 flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-md"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="w-24 h-24 bg-[#76B3A8] rounded-full flex items-center justify-center mx-auto mb-6"
          >
            <CheckCircle className="w-12 h-12 text-white" />
          </motion.div>
          
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-3xl font-bold text-gray-900 mb-4"
          >
            All done!
          </motion.h1>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="mb-6"
          >
            <img
              src="https://images.pexels.com/photos/3768916/pexels-photo-3768916.jpeg?auto=compress&cs=tinysrgb&w=400"
              alt="Success celebration"
              className="w-48 h-32 object-cover rounded-lg mx-auto mb-4"
            />
            <p className="text-xl text-[#76B3A8] font-semibold italic">
              "Halfway to getting guarded!"
            </p>
          </motion.div>
          
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="text-[#7D7F7C]"
          >
            Your basic information has been saved successfully. Let's continue setting up your health profile!
          </motion.p>
        </motion.div>
      </div>
    );
  }

  const currentStepData = steps[currentStep];
  const IconComponent = currentStepData.icon;

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-gray-50 px-4 py-8">
      <div className="max-w-md mx-auto">
        {/* Progress Dots */}
        <div className="flex justify-center mb-8">
          <div className="flex space-x-2">
            {steps.map((_, index) => (
              <motion.div
                key={index}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className={`w-3 h-3 rounded-full transition-all duration-300 ${
                  index <= currentStep ? 'bg-[#76B3A8]' : 'bg-gray-300'
                }`}
              />
            ))}
          </div>
        </div>

        {/* Step Counter */}
        <div className="text-center mb-8">
          <span className="text-sm text-[#7D7F7C]">
            {currentStep + 1} of {steps.length}
          </span>
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
            <div className="text-center mb-8">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                className="inline-flex items-center justify-center w-16 h-16 bg-[#76B3A8] rounded-full mb-4"
              >
                <IconComponent className="w-8 h-8 text-white" />
              </motion.div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                {currentStepData.title}
              </h2>
              <p className="text-[#7D7F7C]">{currentStepData.subtitle}</p>
            </div>

            <div className="space-y-4">
              {currentStepData.type === 'text' && (
                <input
                  type="text"
                  value={basicInfo[currentStepData.id as keyof BasicInfo]}
                  onChange={(e) => updateBasicInfo(currentStepData.id as keyof BasicInfo, e.target.value)}
                  className="w-full px-4 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
                  placeholder={currentStepData.placeholder}
                  autoFocus
                />
              )}

              {currentStepData.type === 'email' && (
                <input
                  type="email"
                  value={basicInfo[currentStepData.id as keyof BasicInfo]}
                  onChange={(e) => updateBasicInfo(currentStepData.id as keyof BasicInfo, e.target.value)}
                  className="w-full px-4 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
                  placeholder={currentStepData.placeholder}
                  autoFocus
                />
              )}

              {currentStepData.type === 'tel' && (
                <input
                  type="tel"
                  value={basicInfo[currentStepData.id as keyof BasicInfo]}
                  onChange={(e) => updateBasicInfo(currentStepData.id as keyof BasicInfo, e.target.value)}
                  className="w-full px-4 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
                  placeholder={currentStepData.placeholder}
                  autoFocus
                />
              )}

              {currentStepData.type === 'date' && (
                <input
                  type="date"
                  value={basicInfo[currentStepData.id as keyof BasicInfo]}
                  onChange={(e) => updateBasicInfo(currentStepData.id as keyof BasicInfo, e.target.value)}
                  className="w-full px-4 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
                  autoFocus
                />
              )}

              {currentStepData.type === 'select' && (
                <div className="space-y-3">
                  {currentStepData.options?.map((option) => (
                    <motion.button
                      key={option.value}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => updateBasicInfo(currentStepData.id as keyof BasicInfo, option.value)}
                      className={`w-full p-4 text-left rounded-lg border-2 transition-all duration-200 ${
                        basicInfo[currentStepData.id as keyof BasicInfo] === option.value
                          ? 'border-[#76B3A8] bg-[#76B3A8]/10'
                          : 'border-gray-200 hover:border-[#76B3A8]/50'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-gray-900 font-medium">{option.label}</span>
                        {basicInfo[currentStepData.id as keyof BasicInfo] === option.value && (
                          <div className="w-6 h-6 bg-[#76B3A8] rounded-full flex items-center justify-center">
                            <div className="w-2 h-2 bg-white rounded-full" />
                          </div>
                        )}
                      </div>
                    </motion.button>
                  ))}
                </div>
              )}

              {currentStepData.type === 'autocomplete' && (
                <div className="relative">
                  <input
                    type="text"
                    value={basicInfo[currentStepData.id as keyof BasicInfo]}
                    onChange={(e) => handleLocationSearch(e.target.value)}
                    className="w-full px-4 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
                    placeholder={currentStepData.placeholder}
                    autoFocus
                  />
                  {locationSuggestions.length > 0 && (
                    <div className="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-lg mt-1 shadow-lg z-10">
                      {locationSuggestions.map((suggestion, index) => (
                        <button
                          key={index}
                          onClick={() => {
                            updateBasicInfo('location', suggestion);
                            setLocationSuggestions([]);
                          }}
                          className="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors duration-200 first:rounded-t-lg last:rounded-b-lg"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
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
            disabled={!isStepValid() || isSubmitting}
            className="flex items-center px-6 py-3 bg-[#76B3A8] text-white rounded-lg font-semibold hover:bg-[#6BA399] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? (
              'Saving...'
            ) : currentStep === steps.length - 1 ? (
              'Complete'
            ) : (
              <>
                Next
                <ChevronRight className="w-5 h-5 ml-2" />
              </>
            )}
          </motion.button>
        </div>
      </div>
    </div>
  );
};