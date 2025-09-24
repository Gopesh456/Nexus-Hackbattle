"use client"

import { Home, Utensils, User, Settings, LogOut } from "lucide-react"
import { cn } from "@/lib/utils"
import { removeAuthToken } from "@/lib/auth"
import { useToast } from "@/hooks/use-toast"

interface NavigationProps {
  currentPage: "home" | "food"
  onPageChange: (page: "home" | "food") => void
}

export function Navigation({ currentPage, onPageChange }: NavigationProps) {
  const { toast } = useToast()

  const handleLogout = () => {
    removeAuthToken()
    localStorage.removeItem("onboarding_complete")
    toast({
      title: "Logged Out",
      description: "You have been successfully logged out.",
    })
    // Reload the page to reset the app state
    window.location.reload()
  }

  const navItems = [
    { id: "home" as const, label: "Home", icon: Home },
    { id: "food" as const, label: "Food Diary", icon: Utensils },
    { id: "profile", label: "Profile", icon: User, disabled: true },
    { id: "settings", label: "Settings", icon: Settings, disabled: true },
  ]

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-card/95 backdrop-blur-sm border-t border-border z-50">
      <div className="flex items-center justify-around py-2">
        {navItems.map((item) => {
          const IconComponent = item.icon
          const isActive = currentPage === item.id

          return (
            <button
              key={item.id}
              onClick={() => !item.disabled && onPageChange(item.id)}
              disabled={item.disabled}
              className={cn(
                "flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-all duration-200",
                isActive
                  ? "text-primary bg-primary/10"
                  : item.disabled
                    ? "text-muted-foreground/50 cursor-not-allowed"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted/50",
              )}
            >
              <IconComponent className="h-5 w-5" />
              <span className="text-xs font-medium">{item.label}</span>
            </button>
          )
        })}

        <button
          onClick={handleLogout}
          className="flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-all duration-200 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
          title="Logout"
        >
          <LogOut className="h-5 w-5" />
          <span className="text-xs font-medium">Logout</span>
        </button>
      </div>
    </nav>
  )
}
