import React from 'react';
import { motion } from 'framer-motion';
import { HealthProfile } from '../../types';

interface GoalsStepProps {
  data: Partial<HealthProfile>;
  onUpdate: (data: Partial<HealthProfile>) => void;
}

const healthGoals = [
  { id: 'weight-loss', label: 'Lose Weight', icon: '⬇️' },
  { id: 'weight-gain', label: 'Gain Weight', icon: '⬆️' },
  { id: 'muscle-gain', label: 'Build Muscle', icon: '💪' },
  { id: 'endurance', label: 'Improve Endurance', icon: '🏃' },
  { id: 'flexibility', label: 'Increase Flexibility', icon: '🧘' },
  { id: 'overall-health', label: 'Overall Health', icon: '❤️' },
  { id: 'stress-reduction', label: 'Reduce Stress', icon: '😌' },
  { id: 'better-sleep', label: 'Better Sleep', icon: '😴' },
];

export const GoalsStep: React.FC<GoalsStepProps> = ({ data, onUpdate }) => {
  const selectedGoals = data.goals || [];

  const toggleGoal = (goalId: string) => {
    const updatedGoals = selectedGoals.includes(goalId)
      ? selectedGoals.filter(g => g !== goalId)
      : [...selectedGoals, goalId];
    
    onUpdate({ goals: updatedGoals });
  };

  return (
    <div className="space-y-6">
      <p className="text-[#7D7F7C]">
        Select your health and fitness goals (you can choose multiple):
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {healthGoals.map((goal, index) => (
          <motion.button
            key={goal.id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => toggleGoal(goal.id)}
            className={`p-4 rounded-lg border-2 transition-all duration-200 ${
              selectedGoals.includes(goal.id)
                ? 'border-[#76B3A8] bg-[#76B3A8]/10'
                : 'border-gray-200 hover:border-[#76B3A8]/50'
            }`}
          >
            <div className="flex items-center space-x-3">
              <span className="text-2xl">{goal.icon}</span>
              <span className="font-medium text-gray-900">{goal.label}</span>
              {selectedGoals.includes(goal.id) && (
                <div className="ml-auto w-6 h-6 bg-[#76B3A8] rounded-full flex items-center justify-center">
                  <div className="w-2 h-2 bg-white rounded-full" />
                </div>
              )}
            </div>
          </motion.button>
        ))}
      </div>

      {selectedGoals.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-[#76B3A8]/10 p-4 rounded-lg"
        >
          <p className="text-sm text-[#7D7F7C]">
            Great! You've selected {selectedGoals.length} goal{selectedGoals.length !== 1 ? 's' : ''}. 
            We'll help you track your progress and provide personalized recommendations.
          </p>
        </motion.div>
      )}
    </div>
  );
};