"use client"

import { useState, useEffect } from "react"
import { AuthForm } from "@/components/auth-form"
import { OnboardingFlow } from "@/components/onboarding-flow"
import { Dashboard } from "@/components/dashboard"
import { getAuthToken } from "@/lib/auth"

export default function Home() {
  const [currentStep, setCurrentStep] = useState<"auth" | "onboarding" | "dashboard">("auth")
  const [baseUrl, setBaseUrl] = useState("")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if user is already authenticated
    const token = getAuthToken()
    if (token) {
      // Check if onboarding is complete (you might want to store this in localStorage)
      const onboardingComplete = localStorage.getItem("onboarding_complete")
      if (onboardingComplete) {
        setCurrentStep("dashboard")
      } else {
        setCurrentStep("onboarding")
      }
    }
    setIsLoading(false)
  }, [])

  const handleAuthSuccess = () => {
    setCurrentStep("onboarding")
  }

  const handleOnboardingComplete = () => {
    localStorage.setItem("onboarding_complete", "true")
    setCurrentStep("dashboard")
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading Nexus Guard...</p>
        </div>
      </div>
    )
  }

  if (currentStep === "auth") {
    return (
      <div>
        {!baseUrl && (
          <div className="fixed top-4 left-4 right-4 z-50">
            <div className="max-w-md mx-auto bg-card border border-border rounded-lg p-4 shadow-lg">
              <label className="block text-sm font-medium mb-2">API Base URL</label>
              <input
                type="url"
                placeholder="https://your-api-domain.com"
                className="w-full px-3 py-2 border border-input rounded-md bg-background"
                onChange={(e) => setBaseUrl(e.target.value)}
              />
            </div>
          </div>
        )}
        {baseUrl && <AuthForm onAuthSuccess={handleAuthSuccess} baseUrl={baseUrl} />}
      </div>
    )
  }

  if (currentStep === "onboarding") {
    return <OnboardingFlow onComplete={handleOnboardingComplete} baseUrl={baseUrl} />
  }

  return <Dashboard baseUrl={baseUrl} />
}
