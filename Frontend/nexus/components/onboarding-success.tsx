"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Shield, Heart, CheckCircle, Sparkles } from "lucide-react"

interface OnboardingSuccessProps {
  onComplete: () => void
}

export function OnboardingSuccess({ onComplete }: OnboardingSuccessProps) {
  const [showQuote, setShowQuote] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setShowQuote(true), 1000)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-2xl text-center">
        <Card className="border-0 shadow-2xl bg-card/90 backdrop-blur-sm animate-fade-in-up">
          <CardHeader className="pb-6">
            <div className="flex justify-center mb-6">
              <div className="relative">
                <div className="p-6 rounded-full bg-primary/10 animate-pulse">
                  <Shield className="h-16 w-16 text-primary" />
                </div>
                <CheckCircle className="h-8 w-8 text-green-500 absolute -top-1 -right-1 bg-background rounded-full" />
              </div>
            </div>
            <CardTitle className="text-3xl font-bold text-balance mb-4">Welcome to Your Health Journey!</CardTitle>
            <div className="space-y-4">
              <div className="flex items-center justify-center gap-2 text-lg text-muted-foreground">
                <Heart className="h-5 w-5 text-red-500" />
                <span>You're halfway to getting guarded</span>
                <Sparkles className="h-5 w-5 text-yellow-500" />
              </div>

              {showQuote && (
                <div className="animate-fade-in-up bg-primary/5 rounded-lg p-6 border border-primary/20">
                  <blockquote className="text-lg italic text-foreground/80 mb-2">
                    "The greatest wealth is health. Your journey to wellness starts with a single step, and you've just
                    taken it."
                  </blockquote>
                  <cite className="text-sm text-muted-foreground">- Nexus Guard</cite>
                </div>
              )}
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
              <div className="p-4 rounded-lg bg-primary/5">
                <Shield className="h-8 w-8 text-primary mx-auto mb-2" />
                <h3 className="font-semibold">Protected</h3>
                <p className="text-sm text-muted-foreground">Your data is secure</p>
              </div>
              <div className="p-4 rounded-lg bg-primary/5">
                <Heart className="h-8 w-8 text-red-500 mx-auto mb-2" />
                <h3 className="font-semibold">Monitored</h3>
                <p className="text-sm text-muted-foreground">24/7 health tracking</p>
              </div>
              <div className="p-4 rounded-lg bg-primary/5">
                <Sparkles className="h-8 w-8 text-yellow-500 mx-auto mb-2" />
                <h3 className="font-semibold">Optimized</h3>
                <p className="text-sm text-muted-foreground">Personalized insights</p>
              </div>
            </div>

            <Button onClick={onComplete} className="w-full h-14 text-lg font-medium">
              Continue to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
