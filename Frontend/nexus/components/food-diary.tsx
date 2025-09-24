"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Plus, Utensils, Coffee, Cookie, Target, Mic, MicOff, Trash2, RefreshCw } from "lucide-react"
import { logNutrition, getNutritionSummary, getAuthToken, type NutritionSummary } from "@/lib/nutrition"
import { NutritionLoadingScreen } from "@/components/nutrition-loading-screen"
import { useToast } from "@/hooks/use-toast"

interface FoodDiaryProps {
  baseUrl: string
}

interface FoodEntry {
  id: string
  name: string
  quantity: number
  unit: string
  calories: number
  protein: number
  carbs: number
  fat: number
  fiber: number
}

interface MealData {
  breakfast: FoodEntry[]
  lunch: FoodEntry[]
  dinner: FoodEntry[]
  snacks: FoodEntry[]
}

const mealIcons = {
  breakfast: Coffee,
  lunch: Utensils,
  dinner: Utensils,
  snacks: Cookie,
}

const units = [
  { value: "g", label: "grams (g)" },
  { value: "kg", label: "kilograms (kg)" },
  { value: "oz", label: "ounces (oz)" },
  { value: "lb", label: "pounds (lb)" },
  { value: "cup", label: "cups" },
  { value: "ml", label: "milliliters (ml)" },
  { value: "l", label: "liters (l)" },
]

const FoodDiary = ({ baseUrl }: FoodDiaryProps) => {
  const [meals, setMeals] = useState<MealData>({
    breakfast: [],
    lunch: [],
    dinner: [],
    snacks: [],
  })

  const [summary, setSummary] = useState<NutritionSummary | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showAddForm, setShowAddForm] = useState<string | null>(null)
  const [isListening, setIsListening] = useState(false)
  const [newFood, setNewFood] = useState({
    name: "",
    quantity: "",
    unit: "g",
  })
  const { toast } = useToast()
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadNutritionSummary()
  }, [])

  const loadNutritionSummary = async () => {
    try {
      setError(null)
      const token = getAuthToken()
      if (!token) {
        setError("Authentication required")
        return
      }

      const summaryData = await getNutritionSummary(token, baseUrl)
      setSummary(summaryData)
    } catch (error) {
      console.error("Failed to load nutrition summary:", error)
      setError("Failed to load nutrition data")
      toast({
        title: "Error",
        description: "Failed to load nutrition summary. Please try again.",
        variant: "destructive",
      })
    }
  }

  const handleAddFood = async (mealType: keyof MealData) => {
    if (!newFood.name || !newFood.quantity) {
      toast({
        title: "Missing Information",
        description: "Please enter both food name and quantity.",
        variant: "destructive",
      })
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const token = getAuthToken()
      if (!token) throw new Error("No auth token")

      const nutritionData = await logNutrition(
        {
          token,
          food_name: newFood.name,
          quantity: Number.parseFloat(newFood.quantity),
          unit: newFood.unit,
        },
        baseUrl,
      )

      const foodEntry: FoodEntry = {
        id: nutritionData.stored_id.toString(),
        name: nutritionData.food_name,
        quantity: nutritionData.quantity,
        unit: nutritionData.unit,
        calories: nutritionData.total_nutrition.calories,
        protein: nutritionData.total_nutrition.protein,
        carbs: nutritionData.total_nutrition.carbohydrates,
        fat: nutritionData.total_nutrition.fat,
        fiber: nutritionData.total_nutrition.fiber,
      }

      setMeals((prev) => ({
        ...prev,
        [mealType]: [...prev[mealType], foodEntry],
      }))

      await loadNutritionSummary()

      setNewFood({ name: "", quantity: "", unit: "g" })
      setShowAddForm(null)

      toast({
        title: "Food Added",
        description: `${nutritionData.food_name} has been added to your ${mealType}.`,
      })
    } catch (error) {
      console.error("Failed to add food:", error)
      setError("Failed to add food. Please try again.")
      toast({
        title: "Error",
        description: "Failed to add food. Please check your connection and try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const startVoiceInput = () => {
    if (!("webkitSpeechRecognition" in window) && !("SpeechRecognition" in window)) {
      toast({
        title: "Voice Input Not Supported",
        description: "Your browser doesn't support voice input. Please type the food name manually.",
        variant: "destructive",
      })
      return
    }

    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition
    const recognition = new SpeechRecognition()

    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = "en-US"

    recognition.onstart = () => {
      setIsListening(true)
      toast({
        title: "Listening...",
        description: "Speak the name of the food you want to add.",
      })
    }

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript
      setNewFood((prev) => ({ ...prev, name: transcript }))
      toast({
        title: "Voice Input Captured",
        description: `Heard: "${transcript}"`,
      })
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognition.onerror = (event: any) => {
      setIsListening(false)
      toast({
        title: "Voice Input Error",
        description: "Could not capture voice input. Please try again or type manually.",
        variant: "destructive",
      })
    }

    recognition.start()
  }

  const removeFood = (mealType: keyof MealData, foodId: string) => {
    setMeals((prev) => ({
      ...prev,
      [mealType]: prev[mealType].filter((food) => food.id !== foodId),
    }))

    toast({
      title: "Food Removed",
      description: "Food item has been removed from your diary.",
    })

    loadNutritionSummary()
  }

  const getMealCalories = (meal: FoodEntry[]) => {
    return meal.reduce((total, food) => total + food.calories, 0)
  }

  const getTotalCalories = () => {
    return Object.values(meals).reduce((total, meal) => total + getMealCalories(meal), 0)
  }

  if (isLoading && showAddForm) {
    return <NutritionLoadingScreen />
  }

  return (
    <div className="p-4 space-y-6 max-w-4xl mx-auto">
      {/* Header with Summary */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-foreground">Food Diary</h1>
          <Button variant="outline" size="sm" onClick={loadNutritionSummary} disabled={isLoading}>
            <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? "animate-spin" : ""}`} />
            Refresh
          </Button>
        </div>

        {error && (
          <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive">
            <p className="text-sm">{error}</p>
          </div>
        )}

        {summary && (
          <Card className="bg-gradient-to-r from-primary/5 to-primary/10 border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5 text-primary" />
                Today's Nutrition Goals
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{Math.round(summary.summary.consumed.calories)}</div>
                  <div className="text-sm text-muted-foreground">/ {summary.summary.goals.calories} cal</div>
                  <Progress value={Math.min(summary.summary.progress.calories_percentage, 100)} className="mt-2 h-2" />
                </div>

                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {Math.round(summary.summary.consumed.protein)}g
                  </div>
                  <div className="text-sm text-muted-foreground">/ {summary.summary.goals.protein}g protein</div>
                  <Progress value={Math.min(summary.summary.progress.protein_percentage, 100)} className="mt-2 h-2" />
                </div>

                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {Math.round(summary.summary.consumed.carbohydrates)}g
                  </div>
                  <div className="text-sm text-muted-foreground">/ {summary.summary.goals.carbohydrates}g carbs</div>
                  <Progress
                    value={Math.min(summary.summary.progress.carbohydrates_percentage, 100)}
                    className="mt-2 h-2"
                  />
                </div>

                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">{Math.round(summary.summary.consumed.fat)}g</div>
                  <div className="text-sm text-muted-foreground">/ {summary.summary.goals.fat}g fat</div>
                  <Progress value={Math.min(summary.summary.progress.fat_percentage, 100)} className="mt-2 h-2" />
                </div>
              </div>

              <div className="text-center">
                <Badge variant="secondary" className="text-sm">
                  {summary.summary.progress.calories_remaining > 0
                    ? `${Math.round(summary.summary.progress.calories_remaining)} calories remaining`
                    : `${Math.abs(Math.round(summary.summary.progress.calories_remaining))} calories over goal`}
                </Badge>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Meals */}
      <div className="space-y-4">
        {Object.entries(meals).map(([mealType, mealFoods]) => {
          const IconComponent = mealIcons[mealType as keyof typeof mealIcons]
          const mealCalories = getMealCalories(mealFoods)

          return (
            <Card key={mealType}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <IconComponent className="h-5 w-5 text-primary" />
                    <span className="capitalize">{mealType}</span>
                    {mealCalories > 0 && <Badge variant="secondary">{Math.round(mealCalories)} cal</Badge>}
                  </div>
                  <Button variant="outline" size="sm" onClick={() => setShowAddForm(mealType)} className="h-8">
                    <Plus className="h-4 w-4 mr-1" />
                    Add Food
                  </Button>
                </CardTitle>
              </CardHeader>

              <CardContent className="space-y-3">
                {mealFoods.length === 0 ? (
                  <p className="text-muted-foreground text-center py-4">No foods logged for {mealType} yet</p>
                ) : (
                  mealFoods.map((food) => (
                    <div key={food.id} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div className="flex-1">
                        <p className="font-medium">{food.name}</p>
                        <p className="text-sm text-muted-foreground">
                          {food.quantity}
                          {food.unit} • {Math.round(food.calories)} cal
                        </p>
                        <div className="text-xs text-muted-foreground mt-1">
                          P: {Math.round(food.protein)}g • C: {Math.round(food.carbs)}g • F: {Math.round(food.fat)}g
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFood(mealType as keyof MealData, food.id)}
                        className="text-destructive hover:text-destructive hover:bg-destructive/10"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  ))
                )}

                {/* Add Food Form */}
                {showAddForm === mealType && (
                  <div className="p-4 border border-border rounded-lg bg-card space-y-3 animate-fade-in-up">
                    <div className="flex items-center gap-2">
                      <Input
                        placeholder="Food name (e.g., banana)"
                        value={newFood.name}
                        onChange={(e) => setNewFood((prev) => ({ ...prev, name: e.target.value }))}
                        className="flex-1"
                        onKeyDown={(e) => {
                          if (e.key === "Enter" && newFood.name && newFood.quantity) {
                            handleAddFood(mealType as keyof MealData)
                          }
                        }}
                      />
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={startVoiceInput}
                        disabled={isListening}
                        className="px-3 bg-transparent"
                        title="Voice input"
                      >
                        {isListening ? (
                          <Mic className="h-4 w-4 text-red-500 animate-pulse" />
                        ) : (
                          <MicOff className="h-4 w-4" />
                        )}
                      </Button>
                    </div>

                    <div className="flex gap-2">
                      <Input
                        type="number"
                        placeholder="Quantity"
                        value={newFood.quantity}
                        onChange={(e) => setNewFood((prev) => ({ ...prev, quantity: e.target.value }))}
                        className="flex-1"
                        min="0"
                        step="0.1"
                        onKeyDown={(e) => {
                          if (e.key === "Enter" && newFood.name && newFood.quantity) {
                            handleAddFood(mealType as keyof MealData)
                          }
                        }}
                      />
                      <Select
                        value={newFood.unit}
                        onValueChange={(value) => setNewFood((prev) => ({ ...prev, unit: value }))}
                      >
                        <SelectTrigger className="w-32">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {units.map((unit) => (
                            <SelectItem key={unit.value} value={unit.value}>
                              {unit.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="flex gap-2">
                      <Button
                        onClick={() => handleAddFood(mealType as keyof MealData)}
                        disabled={!newFood.name || !newFood.quantity || isLoading}
                        className="flex-1"
                      >
                        {isLoading ? "Adding..." : "Add Food"}
                      </Button>
                      <Button
                        variant="outline"
                        onClick={() => {
                          setShowAddForm(null)
                          setNewFood({ name: "", quantity: "", unit: "g" })
                        }}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}

export default FoodDiary
export { FoodDiary }
