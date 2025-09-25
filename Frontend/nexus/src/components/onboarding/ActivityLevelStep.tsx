import React from 'react';
import { motion } from 'framer-motion';
import { HealthProfile } from '../../types';

interface ActivityLevelStepProps {
  data: Partial<HealthProfile>;
  onUpdate: (data: Partial<HealthProfile>) => void;
}

const activityLevels = [
  {
    value: 'sedentary' as const,
    title: 'Sedentary',
    description: 'Little to no exercise, desk job',
    icon: '🪑',
  },
  {
    value: 'light' as const,
    title: 'Light Activity',
    description: 'Light exercise 1-3 days per week',
    icon: '🚶',
  },
  {
    value: 'moderate' as const,
    title: 'Moderate Activity',
    description: 'Moderate exercise 3-5 days per week',
    icon: '🏃',
  },
  {
    value: 'active' as const,
    title: 'Very Active',
    description: 'Hard exercise 6-7 days per week',
    icon: '💪',
  },
  {
    value: 'very-active' as const,
    title: 'Extremely Active',
    description: 'Very hard exercise, physical job',
    icon: '🏋️',
  },
];

export const ActivityLevelStep: React.FC<ActivityLevelStepProps> = ({ data, onUpdate }) => {
  return (
    <div className="space-y-4">
      <p className="text-[#7D7F7C] mb-6">
        Select the option that best describes your current activity level:
      </p>

      <div className="grid gap-4">
        {activityLevels.map((level, index) => (
          <motion.button
            key={level.value}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onUpdate({ activityLevel: level.value })}
            className={`p-4 rounded-lg border-2 text-left transition-all duration-200 ${
              data.activityLevel === level.value
                ? 'border-[#76B3A8] bg-[#76B3A8]/10'
                : 'border-gray-200 hover:border-[#76B3A8]/50'
            }`}
          >
            <div className="flex items-start space-x-4">
              <span className="text-2xl">{level.icon}</span>
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">{level.title}</h3>
                <p className="text-[#7D7F7C] text-sm">{level.description}</p>
              </div>
              {data.activityLevel === level.value && (
                <div className="w-6 h-6 bg-[#76B3A8] rounded-full flex items-center justify-center">
                  <div className="w-2 h-2 bg-white rounded-full" />
                </div>
              )}
            </div>
          </motion.button>
        ))}
      </div>
    </div>
  );
};