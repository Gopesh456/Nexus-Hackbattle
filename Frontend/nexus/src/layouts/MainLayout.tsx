import React, { useState } from "react";
import { Sidebar } from "../components/navigation/Sidebar";
import { DashboardPage } from "../pages/DashboardPage";
import { FoodDiaryPage } from "../pages/FoodDiaryPage";
import { NurseAgentPage } from "../pages/NurseAgentPage";
import { LabMedicationsPage } from "../pages/LabMedicationsPage";
import { ProfilePage } from "../pages/ProfilePage";

export const MainLayout: React.FC = () => {
  const [activePage, setActivePage] = useState("dashboard");

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return <DashboardPage />;
      case "food-diary":
        return <FoodDiaryPage />;
      case "nurse-agent":
        return <NurseAgentPage />;
      case "lab-medications":
        return <LabMedicationsPage />;
      case "profile":
        return <ProfilePage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar activePage={activePage} onPageChange={setActivePage} />
      <div className="flex-1 overflow-auto">{renderPage()}</div>
    </div>
  );
};
