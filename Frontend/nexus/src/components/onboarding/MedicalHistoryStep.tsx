import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { HealthProfile } from '../../types';

interface MedicalHistoryStepProps {
  data: Partial<HealthProfile>;
  onUpdate: (data: Partial<HealthProfile>) => void;
}

const commonConditions = [
  'Diabetes',
  'High Blood Pressure',
  'Heart Disease',
  'Asthma',
  'Arthritis',
  'Allergies',
  'Depression/Anxiety',
  'Sleep Disorders',
];

export const MedicalHistoryStep: React.FC<MedicalHistoryStepProps> = ({ data, onUpdate }) => {
  const [customCondition, setCustomCondition] = useState('');
  const selectedConditions = data.medicalConditions || [];

  const toggleCondition = (condition: string) => {
    const updatedConditions = selectedConditions.includes(condition)
      ? selectedConditions.filter(c => c !== condition)
      : [...selectedConditions, condition];
    
    onUpdate({ medicalConditions: updatedConditions });
  };

  const addCustomCondition = () => {
    if (customCondition.trim() && !selectedConditions.includes(customCondition)) {
      onUpdate({ medicalConditions: [...selectedConditions, customCondition.trim()] });
      setCustomCondition('');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Privacy Notice:</strong> Your medical information is encrypted and never shared with third parties. 
          This helps us provide better, personalized health recommendations.
        </p>
      </div>

      <div>
        <p className="text-[#7D7F7C] mb-4">
          Do you have any of these medical conditions? (Optional)
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {commonConditions.map((condition, index) => (
            <motion.button
              key={condition}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => toggleCondition(condition)}
              className={`p-3 rounded-lg border-2 text-left transition-all duration-200 ${
                selectedConditions.includes(condition)
                  ? 'border-[#76B3A8] bg-[#76B3A8]/10'
                  : 'border-gray-200 hover:border-[#76B3A8]/50'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-gray-900">{condition}</span>
                {selectedConditions.includes(condition) && (
                  <div className="w-5 h-5 bg-[#76B3A8] rounded-full flex items-center justify-center">
                    <div className="w-2 h-2 bg-white rounded-full" />
                  </div>
                )}
              </div>
            </motion.button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Other medical conditions (optional)
        </label>
        <div className="flex gap-2">
          <input
            type="text"
            value={customCondition}
            onChange={(e) => setCustomCondition(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addCustomCondition()}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
            placeholder="Add any other conditions"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={addCustomCondition}
            className="px-4 py-3 bg-[#76B3A8] text-white rounded-lg hover:bg-[#6BA399] transition-colors duration-200"
          >
            Add
          </motion.button>
        </div>
      </div>

      {selectedConditions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-50 p-4 rounded-lg"
        >
          <h4 className="font-medium text-gray-900 mb-2">Selected Conditions:</h4>
          <div className="flex flex-wrap gap-2">
            {selectedConditions.map((condition) => (
              <span
                key={condition}
                className="px-3 py-1 bg-[#76B3A8] text-white text-sm rounded-full"
              >
                {condition}
              </span>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
};