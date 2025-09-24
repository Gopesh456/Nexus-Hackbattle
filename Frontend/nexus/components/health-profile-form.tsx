"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import {
  ChevronLeft,
  ChevronRight,
  Ruler,
  Weight,
  Heart,
  AlertTriangle,
  Pill,
  Droplets,
  Phone,
  User,
} from "lucide-react"
import { storeHealthProfile, getAuthToken } from "@/lib/auth"

interface HealthProfileFormProps {
  onComplete: () => void
  baseUrl: string
}

const questions = [
  {
    id: "height_cm",
    title: "What's your height?",
    subtitle: "In centimeters (e.g., 175 for 5'9\")",
    icon: Ruler,
    type: "number",
    placeholder: "175",
  },
  {
    id: "weight_kg",
    title: "What's your current weight?",
    subtitle: "In kilograms (e.g., 70 for 154 lbs)",
    icon: Weight,
    type: "number",
    placeholder: "70",
  },
  {
    id: "chronic_conditions",
    title: "Do you have any chronic conditions?",
    subtitle: "Type each condition and press comma to add. Leave empty if none.",
    icon: Heart,
    type: "tags",
    placeholder: "Type 2 Diabetes, Hypertension",
  },
  {
    id: "allergies",
    title: "Do you have any allergies?",
    subtitle: "Type each allergy and press comma to add. Leave empty if none.",
    icon: AlertTriangle,
    type: "tags",
    placeholder: "Peanuts, Shellfish",
  },
  {
    id: "current_medications",
    title: "Are you taking any medications?",
    subtitle: "Type each medication and press comma to add. Leave empty if none.",
    icon: Pill,
    type: "tags",
    placeholder: "Metformin 500mg twice daily",
  },
  {
    id: "blood_group",
    title: "What's your blood group?",
    subtitle: "Select your blood type",
    icon: Droplets,
    type: "select",
    options: ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"],
  },
  {
    id: "emergency_contact_name",
    title: "Emergency contact name?",
    subtitle: "Who should we contact in case of emergency?",
    icon: User,
    type: "text",
    placeholder: "John Smith",
  },
  {
    id: "emergency_contact_relationship",
    title: "Relationship to emergency contact?",
    subtitle: "How are they related to you?",
    icon: Heart,
    type: "select",
    options: ["Spouse", "Parent", "Child", "Sibling", "Friend", "Other"],
  },
  {
    id: "emergency_contact_phone",
    title: "Emergency contact phone?",
    subtitle: "Their phone number for emergencies",
    icon: Phone,
    type: "tel",
    placeholder: "+1-555-987-6543",
  },
]

export function HealthProfileForm({ onComplete, baseUrl }: HealthProfileFormProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [formData, setFormData] = useState({
    height_cm: "",
    weight_kg: "",
    chronic_conditions: [] as string[],
    allergies: [] as string[],
    current_medications: [] as string[],
    blood_group: "",
    emergency_contact_name: "",
    emergency_contact_relationship: "",
    emergency_contact_phone: "",
  })
  const [tagInput, setTagInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [slideDirection, setSlideDirection] = useState<"left" | "right">("right")

  const progress = ((currentQuestion + 1) / questions.length) * 100

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setSlideDirection("right")
      setCurrentQuestion(currentQuestion + 1)
      setTagInput("")
    } else {
      handleSubmit()
    }
  }

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setSlideDirection("left")
      setCurrentQuestion(currentQuestion - 1)
      setTagInput("")
    }
  }

  const handleTagInput = (value: string, field: string) => {
    if (value.includes(",")) {
      const newTag = value.replace(",", "").trim()
      if (newTag) {
        setFormData((prev) => ({
          ...prev,
          [field]: [...(prev[field as keyof typeof prev] as string[]), newTag],
        }))
      }
      setTagInput("")
    } else {
      setTagInput(value)
    }
  }

  const removeTag = (index: number, field: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: (prev[field as keyof typeof prev] as string[]).filter((_, i) => i !== index),
    }))
  }

  const handleSubmit = async () => {
    setIsLoading(true)
    try {
      const token = getAuthToken()
      if (!token) throw new Error("No auth token")

      const healthData = {
        token,
        height_cm: Number.parseInt(formData.height_cm),
        weight_kg: Number.parseInt(formData.weight_kg),
        chronic_conditions: formData.chronic_conditions,
        allergies: formData.allergies,
        current_medications: formData.current_medications,
        blood_group: formData.blood_group,
        daily_calorie_goal: 2000, // Default values
        daily_protein_goal: 50,
        daily_carbs_goal: 250,
        daily_fat_goal: 65,
        daily_fiber_goal: 25,
        daily_sugar_goal: 50,
        emergency_contact: {
          name: formData.emergency_contact_name,
          relationship: formData.emergency_contact_relationship,
          phone: formData.emergency_contact_phone,
        },
      }

      await storeHealthProfile(healthData, baseUrl)
      onComplete()
    } catch (error) {
      console.error("Failed to store health profile:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const currentQ = questions[currentQuestion]
  const IconComponent = currentQ.icon

  const isCurrentValid = () => {
    const currentField = currentQ.id
    if (currentQ.type === "tags") {
      return true // Tags are optional
    }
    return (
      formData[currentField as keyof typeof formData] !== "" &&
      formData[currentField as keyof typeof formData] !== undefined
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-muted-foreground">Health Profile</span>
            <span className="text-sm font-medium text-muted-foreground">
              {currentQuestion + 1} of {questions.length}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Question Card */}
        <Card
          className={`border-0 shadow-2xl bg-card/90 backdrop-blur-sm transition-all duration-500 ${
            slideDirection === "right" ? "animate-slide-in-right" : "animate-slide-in-left"
          }`}
          key={currentQuestion}
        >
          <CardHeader className="text-center pb-6">
            <div className="flex justify-center mb-4">
              <div className="p-4 rounded-full bg-primary/10">
                <IconComponent className="h-8 w-8 text-primary" />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold text-balance">{currentQ.title}</CardTitle>
            <p className="text-muted-foreground text-balance">{currentQ.subtitle}</p>
          </CardHeader>

          <CardContent className="space-y-6">
            <div className="space-y-2">
              {currentQ.type === "select" ? (
                <Select
                  value={formData[currentQ.id as keyof typeof formData] as string}
                  onValueChange={(value) => setFormData((prev) => ({ ...prev, [currentQ.id]: value }))}
                >
                  <SelectTrigger className="h-14 text-base">
                    <SelectValue placeholder="Select an option" />
                  </SelectTrigger>
                  <SelectContent>
                    {currentQ.options?.map((option) => (
                      <SelectItem key={option} value={option}>
                        {option}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              ) : currentQ.type === "tags" ? (
                <div className="space-y-3">
                  <Input
                    type="text"
                    placeholder={currentQ.placeholder}
                    value={tagInput}
                    onChange={(e) => handleTagInput(e.target.value, currentQ.id)}
                    className="h-14 text-base"
                    autoFocus
                  />
                  <div className="flex flex-wrap gap-2">
                    {(formData[currentQ.id as keyof typeof formData] as string[]).map((tag, index) => (
                      <Badge
                        key={index}
                        variant="secondary"
                        className="px-3 py-1 cursor-pointer hover:bg-destructive hover:text-destructive-foreground"
                        onClick={() => removeTag(index, currentQ.id)}
                      >
                        {tag} ×
                      </Badge>
                    ))}
                  </div>
                </div>
              ) : (
                <Input
                  type={currentQ.type}
                  placeholder={currentQ.placeholder}
                  value={formData[currentQ.id as keyof typeof formData] as string}
                  onChange={(e) => setFormData((prev) => ({ ...prev, [currentQ.id]: e.target.value }))}
                  className="h-14 text-base"
                  autoFocus
                />
              )}
            </div>

            {/* Navigation Buttons */}
            <div className="flex justify-between pt-4">
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentQuestion === 0}
                className="h-12 px-6 bg-transparent"
              >
                <ChevronLeft className="h-4 w-4 mr-2" />
                Previous
              </Button>

              <Button onClick={handleNext} disabled={!isCurrentValid() || isLoading} className="h-12 px-6">
                {isLoading ? (
                  "Saving..."
                ) : currentQuestion === questions.length - 1 ? (
                  "Complete Profile"
                ) : (
                  <>
                    Next
                    <ChevronRight className="h-4 w-4 ml-2" />
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Pagination Dots */}
        <div className="flex justify-center mt-8 space-x-2">
          {questions.map((_, index) => (
            <div
              key={index}
              className={`h-2 w-2 rounded-full transition-all duration-300 ${
                index === currentQuestion ? "bg-primary w-8" : index < currentQuestion ? "bg-primary/60" : "bg-muted"
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
