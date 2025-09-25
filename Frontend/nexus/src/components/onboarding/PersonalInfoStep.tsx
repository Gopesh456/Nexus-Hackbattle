import React from 'react';
import { HealthProfile } from '../../types';

interface PersonalInfoStepProps {
  data: Partial<HealthProfile>;
  onUpdate: (data: Partial<HealthProfile>) => void;
}

export const PersonalInfoStep: React.FC<PersonalInfoStepProps> = ({ data, onUpdate }) => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Age
          </label>
          <input
            type="number"
            value={data.age || ''}
            onChange={(e) => onUpdate({ age: Number(e.target.value) })}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
            placeholder="Enter your age"
            min="1"
            max="120"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Weight (lbs)
          </label>
          <input
            type="number"
            value={data.weight || ''}
            onChange={(e) => onUpdate({ weight: Number(e.target.value) })}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
            placeholder="Enter your weight"
            min="1"
            max="1000"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Height (inches)
        </label>
        <input
          type="number"
          value={data.height || ''}
          onChange={(e) => onUpdate({ height: Number(e.target.value) })}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
          placeholder="Enter your height in inches"
          min="1"
          max="120"
        />
      </div>

      <div className="text-sm text-[#7D7F7C] bg-gray-50 p-4 rounded-lg">
        <p>This information helps us personalize your health recommendations and track your progress accurately.</p>
      </div>
    </div>
  );
};