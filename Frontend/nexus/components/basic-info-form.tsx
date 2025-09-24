"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Progress } from "@/components/ui/progress"
import { ChevronLeft, ChevronRight, User, Calendar, MapPin, Mail, Phone, Users } from "lucide-react"
import { storeBasicInfo, getAuthToken } from "@/lib/auth"

interface BasicInfoFormProps {
  onComplete: () => void
  baseUrl: string
}

const questions = [
  {
    id: "full_name",
    title: "What's your full name?",
    subtitle: "This helps us personalize your experience",
    icon: User,
    type: "text",
    placeholder: "Enter your full name",
  },
  {
    id: "date_of_birth",
    title: "When were you born?",
    subtitle: "We use this to provide age-appropriate health insights",
    icon: Calendar,
    type: "date",
    placeholder: "",
  },
  {
    id: "gender",
    title: "What's your gender?",
    subtitle: "This helps us provide more accurate health recommendations",
    icon: Users,
    type: "select",
    options: ["Male", "Female", "Non-binary", "Prefer not to say"],
  },
  {
    id: "location",
    title: "Where are you located?",
    subtitle: "City, State, Country format",
    icon: MapPin,
    type: "text",
    placeholder: "New York, NY, USA",
  },
  {
    id: "email",
    title: "What's your email address?",
    subtitle: "We'll use this for important health notifications",
    icon: Mail,
    type: "email",
    placeholder: "your.email@example.com",
  },
  {
    id: "phone",
    title: "What's your phone number?",
    subtitle: "For emergency contacts and important alerts",
    icon: Phone,
    type: "tel",
    placeholder: "+1-555-123-4567",
  },
]

export function BasicInfoForm({ onComplete, baseUrl }: BasicInfoFormProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [formData, setFormData] = useState({
    full_name: "",
    date_of_birth: "",
    gender: "",
    location: "",
    email: "",
    phone: "",
  })
  const [isLoading, setIsLoading] = useState(false)
  const [slideDirection, setSlideDirection] = useState<"left" | "right">("right")

  const progress = ((currentQuestion + 1) / questions.length) * 100

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setSlideDirection("right")
      setCurrentQuestion(currentQuestion + 1)
    } else {
      handleSubmit()
    }
  }

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setSlideDirection("left")
      setCurrentQuestion(currentQuestion - 1)
    }
  }

  const handleSubmit = async () => {
    setIsLoading(true)
    try {
      const token = getAuthToken()
      if (!token) throw new Error("No auth token")

      await storeBasicInfo({ token, ...formData }, baseUrl)
      onComplete()
    } catch (error) {
      console.error("Failed to store basic info:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const currentQ = questions[currentQuestion]
  const IconComponent = currentQ.icon
  const isCurrentValid = formData[currentQ.id as keyof typeof formData].trim() !== ""

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-muted-foreground">Basic Information</span>
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
                  value={formData[currentQ.id as keyof typeof formData]}
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
              ) : (
                <Input
                  type={currentQ.type}
                  placeholder={currentQ.placeholder}
                  value={formData[currentQ.id as keyof typeof formData]}
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

              <Button onClick={handleNext} disabled={!isCurrentValid || isLoading} className="h-12 px-6">
                {isLoading ? (
                  "Saving..."
                ) : currentQuestion === questions.length - 1 ? (
                  "Complete"
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
