"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { login, register, setAuthToken } from "@/lib/auth"
import { Shield, Heart, Activity, Eye, EyeOff } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface AuthFormProps {
  onAuthSuccess: () => void
  baseUrl: string
}

export function AuthForm({ onAuthSuccess, baseUrl }: AuthFormProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [credentials, setCredentials] = useState({
    user: "",
    password: "",
  })
  const { toast } = useToast()

  const handleSubmit = async (isLogin: boolean) => {
    if (!credentials.user || !credentials.password) {
      setError("Please fill in all fields")
      return
    }

    if (credentials.password.length < 6) {
      setError("Password must be at least 6 characters long")
      return
    }

    setIsLoading(true)
    setError("")

    try {
      const response = isLogin ? await login(credentials, baseUrl) : await register(credentials, baseUrl)

      setAuthToken(response.token)
      toast({
        title: isLogin ? "Welcome back!" : "Account created!",
        description: isLogin ? "You have successfully signed in." : "Your account has been created successfully.",
      })
      onAuthSuccess()
    } catch (err) {
      const errorMessage = isLogin
        ? "Login failed. Please check your credentials."
        : "Registration failed. Username might already exist."
      setError(errorMessage)
      toast({
        title: "Authentication Error",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent, isLogin: boolean) => {
    if (e.key === "Enter" && credentials.user && credentials.password) {
      handleSubmit(isLogin)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
      <div className="w-full max-w-md animate-fade-in-up">
        {/* Logo and Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <div className="relative">
              <Shield className="h-12 w-12 text-primary" />
              <Heart className="h-6 w-6 text-primary absolute -top-1 -right-1" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-foreground mb-2">Nexus Guard</h1>
          <p className="text-muted-foreground">Your Personal Health Guardian</p>
        </div>

        <Card className="border-0 shadow-2xl bg-card/80 backdrop-blur-sm">
          <CardHeader className="text-center pb-4">
            <CardTitle className="text-2xl">Welcome</CardTitle>
            <CardDescription>Sign in to your account or create a new one to start your health journey</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="login" className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-6">
                <TabsTrigger value="login">Sign In</TabsTrigger>
                <TabsTrigger value="register">Sign Up</TabsTrigger>
              </TabsList>

              <TabsContent value="login" className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="login-user">Username</Label>
                  <Input
                    id="login-user"
                    type="text"
                    placeholder="Enter your username"
                    value={credentials.user}
                    onChange={(e) => setCredentials((prev) => ({ ...prev, user: e.target.value }))}
                    onKeyDown={(e) => handleKeyDown(e, true)}
                    className="h-12"
                    autoComplete="username"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="login-password">Password</Label>
                  <div className="relative">
                    <Input
                      id="login-password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter your password"
                      value={credentials.password}
                      onChange={(e) => setCredentials((prev) => ({ ...prev, password: e.target.value }))}
                      onKeyDown={(e) => handleKeyDown(e, true)}
                      className="h-12 pr-10"
                      autoComplete="current-password"
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-12 px-3 hover:bg-transparent"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </Button>
                  </div>
                </div>
                {error && (
                  <div className="text-destructive text-sm text-center bg-destructive/10 p-3 rounded-lg">{error}</div>
                )}
                <Button
                  onClick={() => handleSubmit(true)}
                  disabled={isLoading || !credentials.user || !credentials.password}
                  className="w-full h-12 text-base font-medium"
                >
                  {isLoading ? (
                    <div className="flex items-center gap-2">
                      <Activity className="h-4 w-4 animate-spin" />
                      Signing In...
                    </div>
                  ) : (
                    "Sign In"
                  )}
                </Button>
              </TabsContent>

              <TabsContent value="register" className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="register-user">Username</Label>
                  <Input
                    id="register-user"
                    type="text"
                    placeholder="Choose a username"
                    value={credentials.user}
                    onChange={(e) => setCredentials((prev) => ({ ...prev, user: e.target.value }))}
                    onKeyDown={(e) => handleKeyDown(e, false)}
                    className="h-12"
                    autoComplete="username"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-password">Password</Label>
                  <div className="relative">
                    <Input
                      id="register-password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Create a password (min 6 characters)"
                      value={credentials.password}
                      onChange={(e) => setCredentials((prev) => ({ ...prev, password: e.target.value }))}
                      onKeyDown={(e) => handleKeyDown(e, false)}
                      className="h-12 pr-10"
                      autoComplete="new-password"
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-12 px-3 hover:bg-transparent"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </Button>
                  </div>
                  {credentials.password && credentials.password.length < 6 && (
                    <p className="text-xs text-muted-foreground">Password must be at least 6 characters</p>
                  )}
                </div>
                {error && (
                  <div className="text-destructive text-sm text-center bg-destructive/10 p-3 rounded-lg">{error}</div>
                )}
                <Button
                  onClick={() => handleSubmit(false)}
                  disabled={isLoading || !credentials.user || credentials.password.length < 6}
                  className="w-full h-12 text-base font-medium"
                >
                  {isLoading ? (
                    <div className="flex items-center gap-2">
                      <Activity className="h-4 w-4 animate-spin" />
                      Creating Account...
                    </div>
                  ) : (
                    "Create Account"
                  )}
                </Button>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        <div className="text-center mt-6 text-sm text-muted-foreground">
          <p>Secure • Private • HIPAA Compliant</p>
        </div>
      </div>
    </div>
  )
}
