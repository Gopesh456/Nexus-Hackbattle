import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BasicInfoFlow } from '../components/onboarding/BasicInfoFlow';
import { HealthProfileFlow } from '../components/onboarding/HealthProfileFlow';

export const Onboarding: React.FC = () => {
  const navigate = useNavigate();
  const [showHealthProfile, setShowHealthProfile] = useState(false);

  const handleBasicInfoComplete = () => {
    setShowHealthProfile(true);
  };

  const handleHealthProfileComplete = () => {
    navigate('/dashboard');
  };

  if (showHealthProfile) {
    return <HealthProfileFlow onComplete={handleHealthProfileComplete} />;
  }

  return (
    <BasicInfoFlow onComplete={handleBasicInfoComplete} />
  );
};