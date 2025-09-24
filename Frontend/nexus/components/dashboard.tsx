"use client"

import { useState } from "react"
import { DashboardHome } from "@/components/dashboard-home"
import { FoodDiary } from "@/components/food-diary"
import { Navigation } from "@/components/navigation"

interface DashboardProps {
  baseUrl: string
}

export function Dashboard({ baseUrl }: DashboardProps) {
  const [currentPage, setCurrentPage] = useState<"home" | "food">("home")

  return (
    <div className="min-h-screen bg-background">
      <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />

      <main className="pb-20">
        {currentPage === "home" && <DashboardHome baseUrl={baseUrl} />}
        {currentPage === "food" && <FoodDiary baseUrl={baseUrl} />}
      </main>
    </div>
  )
}
