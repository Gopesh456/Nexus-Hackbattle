"use client"

import { useState } from "react"
import { BasicInfoForm } from "@/components/basic-info-form"
import { HealthProfileForm } from "@/components/health-profile-form"
import { OnboardingSuccess } from "@/components/onboarding-success"

interface OnboardingFlowProps {
  onComplete: () => void
  baseUrl: string
}

export function OnboardingFlow({ onComplete, baseUrl }: OnboardingFlowProps) {
  const [currentStep, setCurrentStep] = useState<"basic" | "health" | "success">("basic")

  const handleBasicInfoComplete = () => {
    setCurrentStep("health")
  }

  const handleHealthProfileComplete = () => {
    setCurrentStep("success")
  }

  const handleSuccessComplete = () => {
    onComplete()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      {currentStep === "basic" && <BasicInfoForm onComplete={handleBasicInfoComplete} baseUrl={baseUrl} />}
      {currentStep === "health" && <HealthProfileForm onComplete={handleHealthProfileComplete} baseUrl={baseUrl} />}
      {currentStep === "success" && <OnboardingSuccess onComplete={handleSuccessComplete} />}
    </div>
  )
}
