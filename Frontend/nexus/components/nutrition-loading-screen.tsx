"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Utensils, Zap, Target } from "lucide-react"

const loadingMessages = [
  "Analyzing nutritional content...",
  "Calculating macronutrients...",
  "Fetching USDA database...",
  "Processing food data...",
  "Almost ready...",
]

const nutritionFacts = [
  "Did you know? Protein helps build and repair tissues in your body.",
  "Fiber aids in digestion and helps maintain healthy cholesterol levels.",
  "Complex carbohydrates provide sustained energy throughout the day.",
  "Healthy fats are essential for brain function and hormone production.",
  "Vitamins and minerals support immune system function.",
]

export function NutritionLoadingScreen() {
  const [progress, setProgress] = useState(0)
  const [messageIndex, setMessageIndex] = useState(0)
  const [factIndex, setFactIndex] = useState(0)

  useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) return 100
        return prev + Math.random() * 15
      })
    }, 200)

    const messageInterval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % loadingMessages.length)
    }, 800)

    const factInterval = setInterval(() => {
      setFactIndex((prev) => (prev + 1) % nutritionFacts.length)
    }, 2000)

    return () => {
      clearInterval(progressInterval)
      clearInterval(messageInterval)
      clearInterval(factInterval)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <Card className="border-0 shadow-2xl bg-card/90 backdrop-blur-sm">
          <CardContent className="p-8 text-center space-y-6">
            {/* Animated Icon */}
            <div className="relative">
              <div className="p-6 rounded-full bg-primary/10 animate-pulse">
                <Utensils className="h-12 w-12 text-primary mx-auto" />
              </div>
              <div className="absolute -top-2 -right-2 p-2 rounded-full bg-green-100 dark:bg-green-900/20 animate-bounce">
                <Zap className="h-4 w-4 text-green-600" />
              </div>
            </div>

            {/* Loading Message */}
            <div className="space-y-2">
              <h3 className="text-xl font-semibold text-foreground">Processing Your Food</h3>
              <p className="text-muted-foreground animate-pulse">{loadingMessages[messageIndex]}</p>
            </div>

            {/* Progress Bar */}
            <div className="space-y-2">
              <Progress value={Math.min(progress, 100)} className="h-3" />
              <p className="text-sm text-muted-foreground">{Math.round(Math.min(progress, 100))}% complete</p>
            </div>

            {/* Nutrition Fact */}
            <div className="p-4 rounded-lg bg-primary/5 border border-primary/20">
              <div className="flex items-start gap-2">
                <Target className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                <p className="text-sm text-foreground/80 text-left">{nutritionFacts[factIndex]}</p>
              </div>
            </div>

            {/* Loading Indicators */}
            <div className="flex justify-center space-x-2">
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  className="h-2 w-2 rounded-full bg-primary animate-bounce"
                  style={{ animationDelay: `${i * 0.2}s` }}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
