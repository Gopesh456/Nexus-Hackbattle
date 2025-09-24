"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Heart, Activity, Thermometer, Droplets, Moon, Footprints, Clock, TrendingUp, Shield, Zap } from "lucide-react"
import { cn } from "@/lib/utils"

interface DashboardHomeProps {
  baseUrl: string
}

interface SmartWatchData {
  heartRate: number
  steps: number
  calories: number
  temperature: number
  oxygenSaturation: number
  sleepHours: number
  activeMinutes: number
  timestamp: string
}

export function DashboardHome({ baseUrl }: DashboardHomeProps) {
  const [smartWatchData, setSmartWatchData] = useState<SmartWatchData>({
    heartRate: 72,
    steps: 8420,
    calories: 1850,
    temperature: 98.6,
    oxygenSaturation: 98,
    sleepHours: 7.5,
    activeMinutes: 45,
    timestamp: new Date().toISOString(),
  })

  const [isConnected, setIsConnected] = useState(true)
  const [connectionAttempts, setConnectionAttempts] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      const shouldDisconnect = Math.random() < 0.05

      if (shouldDisconnect && connectionAttempts < 3) {
        setIsConnected(false)
        setConnectionAttempts((prev) => prev + 1)

        setTimeout(
          () => {
            setIsConnected(true)
            setConnectionAttempts(0)
          },
          Math.random() * 3000 + 2000,
        )
      } else {
        setSmartWatchData((prev) => ({
          ...prev,
          heartRate: Math.floor(Math.random() * 20) + 65,
          steps: prev.steps + Math.floor(Math.random() * 10),
          calories: prev.calories + Math.floor(Math.random() * 5),
          temperature: 98.6 + (Math.random() - 0.5) * 2,
          oxygenSaturation: Math.floor(Math.random() * 3) + 97,
          activeMinutes: prev.activeMinutes + (Math.random() > 0.7 ? 1 : 0),
          timestamp: new Date().toISOString(),
        }))
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [connectionAttempts])

  const getHeartRateStatus = (hr: number) => {
    if (hr < 60) return { status: "Low", color: "text-blue-500" }
    if (hr > 100) return { status: "High", color: "text-red-500" }
    return { status: "Normal", color: "text-green-500" }
  }

  const heartRateStatus = getHeartRateStatus(smartWatchData.heartRate)

  return (
    <div className="p-4 space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Good morning!</h1>
          <p className="text-muted-foreground">Here's your health overview for today</p>
        </div>
        <div className="flex items-center gap-2">
          <div className={`h-2 w-2 rounded-full ${isConnected ? "bg-green-500" : "bg-red-500"} animate-pulse`} />
          <span className="text-sm text-muted-foreground">
            {isConnected ? "Connected" : `Reconnecting... (${connectionAttempts}/3)`}
          </span>
        </div>
      </div>

      {!isConnected && (
        <div className="p-4 rounded-lg bg-yellow-50 dark:bg-yellow-950/20 border border-yellow-200 dark:border-yellow-800">
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-yellow-600" />
            <p className="text-sm font-medium text-yellow-800 dark:text-yellow-200">Smartwatch Connection Lost</p>
          </div>
          <p className="text-xs text-yellow-600 dark:text-yellow-400 mt-1">
            Attempting to reconnect to your device. Please ensure your smartwatch is nearby and Bluetooth is enabled.
          </p>
        </div>
      )}

      {/* Live Vitals */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card
          className={cn(
            "bg-gradient-to-br from-red-50 to-red-100 dark:from-red-950/20 dark:to-red-900/20 border-red-200 dark:border-red-800",
            !isConnected && "opacity-60",
          )}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Heart Rate</CardTitle>
            <Heart className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{smartWatchData.heartRate} BPM</div>
            <p className={`text-xs ${heartRateStatus.color}`}>{heartRateStatus.status}</p>
          </CardContent>
        </Card>

        <Card
          className={cn(
            "bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950/20 dark:to-blue-900/20 border-blue-200 dark:border-blue-800",
            !isConnected && "opacity-60",
          )}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Steps</CardTitle>
            <Footprints className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{smartWatchData.steps.toLocaleString()}</div>
            <Progress value={(smartWatchData.steps / 10000) * 100} className="mt-2 h-1" />
            <p className="text-xs text-muted-foreground mt-1">Goal: 10,000 steps</p>
          </CardContent>
        </Card>

        <Card
          className={cn(
            "bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-950/20 dark:to-orange-900/20 border-orange-200 dark:border-orange-800",
            !isConnected && "opacity-60",
          )}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Calories</CardTitle>
            <Zap className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{smartWatchData.calories}</div>
            <p className="text-xs text-muted-foreground">Burned today</p>
          </CardContent>
        </Card>

        <Card
          className={cn(
            "bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950/20 dark:to-green-900/20 border-green-200 dark:border-green-800",
            !isConnected && "opacity-60",
          )}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Oxygen</CardTitle>
            <Droplets className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{smartWatchData.oxygenSaturation}%</div>
            <p className="text-xs text-green-600">Excellent</p>
          </CardContent>
        </Card>
      </div>

      {/* Today's Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-primary" />
            Today's Summary
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
              <div className="p-2 rounded-full bg-purple-100 dark:bg-purple-900/20">
                <Moon className="h-4 w-4 text-purple-600" />
              </div>
              <div>
                <p className="text-sm font-medium">Sleep</p>
                <p className="text-lg font-bold">{smartWatchData.sleepHours}h</p>
                <p className="text-xs text-muted-foreground">Good quality</p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
              <div className="p-2 rounded-full bg-indigo-100 dark:bg-indigo-900/20">
                <Activity className="h-4 w-4 text-indigo-600" />
              </div>
              <div>
                <p className="text-sm font-medium">Active Minutes</p>
                <p className="text-lg font-bold">{smartWatchData.activeMinutes}</p>
                <p className="text-xs text-muted-foreground">Goal: 60 min</p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
              <div className="p-2 rounded-full bg-yellow-100 dark:bg-yellow-900/20">
                <Thermometer className="h-4 w-4 text-yellow-600" />
              </div>
              <div>
                <p className="text-sm font-medium">Temperature</p>
                <p className="text-lg font-bold">{smartWatchData.temperature.toFixed(1)}°F</p>
                <p className="text-xs text-muted-foreground">Normal range</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Health Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-primary" />
            Health Insights
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-start gap-3 p-3 rounded-lg bg-green-50 dark:bg-green-950/20 border border-green-200 dark:border-green-800">
            <div className="p-1 rounded-full bg-green-100 dark:bg-green-900/20 mt-0.5">
              <TrendingUp className="h-3 w-3 text-green-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-green-800 dark:text-green-200">Great Progress!</p>
              <p className="text-xs text-green-600 dark:text-green-400">
                Your heart rate variability has improved by 12% this week.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 rounded-lg bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800">
            <div className="p-1 rounded-full bg-blue-100 dark:bg-blue-900/20 mt-0.5">
              <Footprints className="h-3 w-3 text-blue-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-blue-800 dark:text-blue-200">Step Goal Achievement</p>
              <p className="text-xs text-blue-600 dark:text-blue-400">
                You're {Math.round((smartWatchData.steps / 10000) * 100)}% towards your daily step goal.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 rounded-lg bg-orange-50 dark:bg-orange-950/20 border border-orange-200 dark:border-orange-800">
            <div className="p-1 rounded-full bg-orange-100 dark:bg-orange-900/20 mt-0.5">
              <Clock className="h-3 w-3 text-orange-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-orange-800 dark:text-orange-200">Hydration Reminder</p>
              <p className="text-xs text-orange-600 dark:text-orange-400">
                Remember to drink water regularly throughout the day.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Last Updated */}
      <div className="text-center text-xs text-muted-foreground">
        Last updated: {new Date(smartWatchData.timestamp).toLocaleTimeString()}
      </div>
    </div>
  )
}
