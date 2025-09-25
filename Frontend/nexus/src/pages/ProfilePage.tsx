import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  User,
  Mail,
  Phone,
  MapPin,
  Calendar,
  Users,
  Edit3,
  Save,
  X,
  Plus,
  Clock,
  FileText,
  Download,
  Trash2,
  CheckCircle,
  Heart,
  Activity,
  Scale,
  Ruler,
  AlertTriangle,
  Pill,
  Droplets,
  Target,
} from "lucide-react";
import { apiClient } from "../utils/api";

interface UserProfile {
  full_name: string;
  email: string;
  phone: string;
  location: string;
  date_of_birth: string;
  gender: string;
}

interface HealthProfile {
  height_cm: number;
  weight_kg: number;
  chronic_conditions: string[];
  allergies: string[];
  current_medications: string[];
  blood_group: string;
  daily_calorie_goal: number;
  daily_protein_goal: number;
  emergency_contact: {
    name: string;
    relationship: string;
    phone: string;
  };
}

interface Appointment {
  id: string;
  doctorName: string;
  specialty: string;
  date: string;
  time: string;
  type: string;
  status: "upcoming" | "completed" | "cancelled";
  notes?: string;
  location?: string;
}

interface EditingAppointment extends Partial<Appointment> {
  id?: string;
}

export const ProfilePage: React.FC = () => {
  const [profile, setProfile] = useState<UserProfile>({
    full_name: "",
    email: "",
    phone: "",
    location: "",
    date_of_birth: "",
    gender: "",
  });

  const [healthProfile, setHealthProfile] = useState<HealthProfile>({
    height_cm: 0,
    weight_kg: 0,
    chronic_conditions: [],
    allergies: [],
    current_medications: [],
    blood_group: "",
    daily_calorie_goal: 0,
    daily_protein_goal: 0,
    emergency_contact: {
      name: "",
      relationship: "",
      phone: "",
    },
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch profile data on component mount
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setLoading(true);

        // Fetch basic info
        const basicInfoResponse = await apiClient.getBasicInfo();
        if (basicInfoResponse) {
          setProfile(basicInfoResponse);
        }

        // Fetch health profile
        const healthProfileResponse = await apiClient.getHealthProfile();
        if (healthProfileResponse) {
          setHealthProfile(healthProfileResponse);
        }

        setError(null);
      } catch (err) {
        console.error("Failed to fetch profile data:", err);
        setError("Failed to load profile data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, []);

  const [appointments, setAppointments] = useState<Appointment[]>([
    {
      id: "1",
      doctorName: "Dr. Sarah Smith",
      specialty: "Cardiologist",
      date: "2025-09-26",
      time: "14:00",
      type: "Consultation",
      status: "upcoming",
      notes: "Routine check-up for blood pressure monitoring",
      location: "Cardiology Center, 123 Medical St.",
    },
    {
      id: "2",
      doctorName: "Dr. Michael Johnson",
      specialty: "Endocrinologist",
      date: "2025-10-03",
      time: "10:30",
      type: "Follow-up",
      status: "upcoming",
      notes: "Diabetes management and medication adjustment",
      location: "Diabetes Care Clinic, 456 Health Ave.",
    },
    {
      id: "3",
      doctorName: "Dr. Emily Davis",
      specialty: "General Practitioner",
      date: "2025-09-20",
      time: "11:00",
      type: "Annual Physical",
      status: "completed",
      notes: "Annual health screening completed successfully",
      location: "Main Health Center, 789 Wellness Blvd.",
    },
  ]);

  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [editingAppointment, setEditingAppointment] =
    useState<EditingAppointment | null>(null);
  const [showAppointmentForm, setShowAppointmentForm] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);

  const upcomingAppointments = appointments.filter(
    (apt) => apt.status === "upcoming"
  );
  const pastAppointments = appointments.filter(
    (apt) => apt.status === "completed" || apt.status === "cancelled"
  );

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const getStatusColor = (status: Appointment["status"]) => {
    switch (status) {
      case "upcoming":
        return "text-blue-700 bg-blue-100 border-blue-200";
      case "completed":
        return "text-green-700 bg-green-100 border-green-200";
      case "cancelled":
        return "text-red-700 bg-red-100 border-red-200";
      default:
        return "text-gray-700 bg-gray-100 border-gray-200";
    }
  };

  const handleProfileSave = async () => {
    try {
      await apiClient.updateBasicInfo({ ...profile });
      setIsEditingProfile(false);
      // Show success message (you could add a toast notification here)
    } catch (err) {
      console.error("Failed to update profile:", err);
      alert("Failed to update profile. Please try again.");
    }
  };

  const handleAppointmentSave = () => {
    if (!editingAppointment) return;

    if (editingAppointment.id) {
      // Update existing appointment
      setAppointments((prev) =>
        prev.map((apt) =>
          apt.id === editingAppointment.id
            ? ({ ...apt, ...editingAppointment } as Appointment)
            : apt
        )
      );
    } else {
      // Add new appointment
      const newAppointment: Appointment = {
        ...editingAppointment,
        id: Date.now().toString(),
        status: "upcoming",
      } as Appointment;
      setAppointments((prev) => [...prev, newAppointment]);
    }

    setEditingAppointment(null);
    setShowAppointmentForm(false);
  };

  const handleAppointmentDelete = (id: string) => {
    setAppointments((prev) => prev.filter((apt) => apt.id !== id));
  };

  const handleDownloadHealthSummary = async () => {
    setIsDownloading(true);

    // Simulate API call for PDF generation
    setTimeout(() => {
      // In a real app, this would call the API with JWT token
      // fetch('/api/health-summary/pdf', {
      //   headers: { 'Authorization': `Bearer ${token}` }
      // })

      // Simulate file download
      const link = document.createElement("a");
      link.href = "#"; // This would be the actual PDF blob URL
      link.download = "health-summary.pdf";
      // link.click();

      setIsDownloading(false);
      alert("Health summary download started!"); // Replace with actual download
    }, 2000);
  };

  // Show loading state
  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#76B3A8] mx-auto mb-4"></div>
            <p className="text-gray-600">Loading profile data...</p>
          </div>
        </div>
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-lg font-semibold text-gray-900 mb-2">
              Error Loading Profile
            </h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-[#76B3A8] text-white rounded-lg hover:bg-[#6ba396] transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Profile</h1>
          <p className="text-gray-600">
            Manage your personal information and appointments
          </p>
        </div>
      </div>

      {/* Personal Information Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
      >
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">
              Personal Information
            </h2>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setIsEditingProfile(!isEditingProfile)}
              className="flex items-center space-x-2 text-[#76B3A8] hover:text-[#6ba396] transition-colors"
            >
              {isEditingProfile ? (
                <>
                  <X className="w-4 h-4" />
                  <span>Cancel</span>
                </>
              ) : (
                <>
                  <Edit3 className="w-4 h-4" />
                  <span>Edit</span>
                </>
              )}
            </motion.button>
          </div>
        </div>

        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <User className="w-4 h-4 inline mr-2" />
                Full Name
              </label>
              {isEditingProfile ? (
                <input
                  type="text"
                  value={profile.full_name}
                  onChange={(e) =>
                    setProfile((prev) => ({
                      ...prev,
                      full_name: e.target.value,
                    }))
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                />
              ) : (
                <p className="text-gray-900 py-3">{profile.full_name}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Mail className="w-4 h-4 inline mr-2" />
                Email
              </label>
              {isEditingProfile ? (
                <input
                  type="email"
                  value={profile.email}
                  onChange={(e) =>
                    setProfile((prev) => ({ ...prev, email: e.target.value }))
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                />
              ) : (
                <p className="text-gray-900 py-3">{profile.email}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Phone className="w-4 h-4 inline mr-2" />
                Phone
              </label>
              {isEditingProfile ? (
                <input
                  type="tel"
                  value={profile.phone}
                  onChange={(e) =>
                    setProfile((prev) => ({ ...prev, phone: e.target.value }))
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                />
              ) : (
                <p className="text-gray-900 py-3">{profile.phone}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPin className="w-4 h-4 inline mr-2" />
                Location
              </label>
              {isEditingProfile ? (
                <input
                  type="text"
                  value={profile.location}
                  onChange={(e) =>
                    setProfile((prev) => ({
                      ...prev,
                      location: e.target.value,
                    }))
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                />
              ) : (
                <p className="text-gray-900 py-3">{profile.location}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="w-4 h-4 inline mr-2" />
                Date of Birth
              </label>
              {isEditingProfile ? (
                <input
                  type="date"
                  value={profile.date_of_birth}
                  onChange={(e) =>
                    setProfile((prev) => ({
                      ...prev,
                      date_of_birth: e.target.value,
                    }))
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                />
              ) : (
                <p className="text-gray-900 py-3">
                  {formatDate(profile.date_of_birth)}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Users className="w-4 h-4 inline mr-2" />
                Gender
              </label>
              {isEditingProfile ? (
                <select
                  value={profile.gender}
                  onChange={(e) =>
                    setProfile((prev) => ({ ...prev, gender: e.target.value }))
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="non-binary">Non-binary</option>
                  <option value="prefer-not-to-say">Prefer not to say</option>
                </select>
              ) : (
                <p className="text-gray-900 py-3 capitalize">
                  {profile.gender}
                </p>
              )}
            </div>
          </div>

          {isEditingProfile && (
            <div className="flex justify-end space-x-3 mt-6 pt-6 border-t border-gray-100">
              <button
                onClick={() => setIsEditingProfile(false)}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleProfileSave}
                className="flex items-center space-x-2 px-6 py-2 bg-[#76B3A8] text-white rounded-lg hover:bg-[#6ba396] transition-colors"
              >
                <Save className="w-4 h-4" />
                <span>Save Changes</span>
              </motion.button>
            </div>
          )}
        </div>
      </motion.div>

      {/* Health Profile Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200"
      >
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center">
              <Heart className="w-5 h-5 mr-2 text-red-500" />
              Health Profile
            </h2>
          </div>
        </div>

        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Physical Measurements */}
            <div className="space-y-4">
              <h3 className="font-medium text-gray-900 flex items-center">
                <Activity className="w-4 h-4 mr-2 text-blue-600" />
                Physical Measurements
              </h3>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  <Ruler className="w-3 h-3 inline mr-1" />
                  Height
                </label>
                <p className="text-gray-900">
                  {healthProfile.height_cm
                    ? `${healthProfile.height_cm} cm`
                    : "Not specified"}
                </p>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  <Scale className="w-3 h-3 inline mr-1" />
                  Weight
                </label>
                <p className="text-gray-900">
                  {healthProfile.weight_kg
                    ? `${healthProfile.weight_kg} kg`
                    : "Not specified"}
                </p>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  <Droplets className="w-3 h-3 inline mr-1" />
                  Blood Group
                </label>
                <p className="text-gray-900">
                  {healthProfile.blood_group || "Not specified"}
                </p>
              </div>
            </div>

            {/* Medical Information */}
            <div className="space-y-4">
              <h3 className="font-medium text-gray-900 flex items-center">
                <AlertTriangle className="w-4 h-4 mr-2 text-orange-600" />
                Medical Information
              </h3>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  Chronic Conditions
                </label>
                <div className="text-gray-900">
                  {healthProfile.chronic_conditions &&
                  healthProfile.chronic_conditions.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {healthProfile.chronic_conditions.map(
                        (condition, index) => (
                          <span
                            key={index}
                            className="inline-block px-2 py-1 bg-red-100 text-red-700 text-xs rounded-full"
                          >
                            {condition}
                          </span>
                        )
                      )}
                    </div>
                  ) : (
                    <span>None reported</span>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  Allergies
                </label>
                <div className="text-gray-900">
                  {healthProfile.allergies &&
                  healthProfile.allergies.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {healthProfile.allergies.map((allergy, index) => (
                        <span
                          key={index}
                          className="inline-block px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded-full"
                        >
                          {allergy}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span>None reported</span>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  <Pill className="w-3 h-3 inline mr-1" />
                  Current Medications
                </label>
                <div className="text-gray-900">
                  {healthProfile.current_medications &&
                  healthProfile.current_medications.length > 0 ? (
                    <div className="space-y-1">
                      {healthProfile.current_medications.map(
                        (medication, index) => (
                          <div key={index} className="text-sm">
                            • {medication}
                          </div>
                        )
                      )}
                    </div>
                  ) : (
                    <span>None reported</span>
                  )}
                </div>
              </div>
            </div>

            {/* Goals & Emergency */}
            <div className="space-y-4">
              <h3 className="font-medium text-gray-900 flex items-center">
                <Target className="w-4 h-4 mr-2 text-green-600" />
                Goals & Emergency
              </h3>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  Daily Calorie Goal
                </label>
                <p className="text-gray-900">
                  {healthProfile.daily_calorie_goal
                    ? `${healthProfile.daily_calorie_goal} kcal`
                    : "Not set"}
                </p>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  Daily Protein Goal
                </label>
                <p className="text-gray-900">
                  {healthProfile.daily_protein_goal
                    ? `${healthProfile.daily_protein_goal} g`
                    : "Not set"}
                </p>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">
                  <Phone className="w-3 h-3 inline mr-1" />
                  Emergency Contact
                </label>
                <div className="text-gray-900">
                  {healthProfile.emergency_contact &&
                  healthProfile.emergency_contact.name ? (
                    <div className="space-y-1 text-sm">
                      <div>
                        <strong>{healthProfile.emergency_contact.name}</strong>
                      </div>
                      <div className="text-gray-600">
                        {healthProfile.emergency_contact.relationship}
                      </div>
                      <div className="text-gray-600">
                        {healthProfile.emergency_contact.phone}
                      </div>
                    </div>
                  ) : (
                    <span>Not specified</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Appointments Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200"
      >
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">
              Appointments
            </h2>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => {
                setEditingAppointment({
                  doctorName: "",
                  specialty: "",
                  date: "",
                  time: "",
                  type: "",
                  notes: "",
                  location: "",
                });
                setShowAppointmentForm(true);
              }}
              className="flex items-center space-x-2 bg-[#76B3A8] text-white px-4 py-2 rounded-lg hover:bg-[#6ba396] transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add Appointment</span>
            </motion.button>
          </div>
        </div>

        <div className="p-6">
          {/* Upcoming Appointments */}
          <div className="mb-8">
            <h3 className="text-md font-semibold text-gray-900 mb-4 flex items-center">
              <Clock className="w-5 h-5 mr-2 text-blue-600" />
              Upcoming Appointments ({upcomingAppointments.length})
            </h3>

            {upcomingAppointments.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Calendar className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>No upcoming appointments</p>
              </div>
            ) : (
              <div className="space-y-4">
                {upcomingAppointments.map((appointment) => (
                  <motion.div
                    key={appointment.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h4 className="font-semibold text-gray-900">
                            {appointment.doctorName}
                          </h4>
                          <span
                            className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium border ${getStatusColor(
                              appointment.status
                            )}`}
                          >
                            {appointment.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mb-1">
                          {appointment.specialty} • {appointment.type}
                        </p>
                        <p className="text-sm text-gray-600 mb-1">
                          {formatDate(appointment.date)} at {appointment.time}
                        </p>
                        {appointment.location && (
                          <p className="text-sm text-gray-500 mb-2">
                            {appointment.location}
                          </p>
                        )}
                        {appointment.notes && (
                          <p className="text-sm text-gray-600 italic">
                            {appointment.notes}
                          </p>
                        )}
                      </div>

                      <div className="flex items-center space-x-1 ml-4">
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          onClick={() => {
                            setEditingAppointment(appointment);
                            setShowAppointmentForm(true);
                          }}
                          className="p-2 text-gray-400 hover:text-[#76B3A8] transition-colors"
                          title="Edit appointment"
                        >
                          <Edit3 className="w-4 h-4" />
                        </motion.button>
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          onClick={() =>
                            handleAppointmentDelete(appointment.id)
                          }
                          className="p-2 text-gray-400 hover:text-red-500 transition-colors"
                          title="Delete appointment"
                        >
                          <Trash2 className="w-4 h-4" />
                        </motion.button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </div>

          {/* Past Appointments */}
          <div>
            <h3 className="text-md font-semibold text-gray-900 mb-4 flex items-center">
              <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
              Past Appointments ({pastAppointments.length})
            </h3>

            {pastAppointments.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <FileText className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>No past appointments</p>
              </div>
            ) : (
              <div className="space-y-4">
                {pastAppointments.map((appointment) => (
                  <motion.div
                    key={appointment.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="border border-gray-200 rounded-lg p-4 bg-gray-50"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h4 className="font-semibold text-gray-700">
                            {appointment.doctorName}
                          </h4>
                          <span
                            className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium border ${getStatusColor(
                              appointment.status
                            )}`}
                          >
                            {appointment.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mb-1">
                          {appointment.specialty} • {appointment.type}
                        </p>
                        <p className="text-sm text-gray-600 mb-1">
                          {formatDate(appointment.date)} at {appointment.time}
                        </p>
                        {appointment.notes && (
                          <p className="text-sm text-gray-600 italic">
                            {appointment.notes}
                          </p>
                        )}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </div>
        </div>
      </motion.div>

      {/* Health Summary Download */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200"
      >
        <div className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                Health Summary
              </h2>
              <p className="text-gray-600 mt-1">
                Download a comprehensive PDF report of your health data
              </p>
            </div>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleDownloadHealthSummary}
              disabled={isDownloading}
              className="flex items-center space-x-2 bg-[#76B3A8] text-white px-6 py-3 rounded-lg hover:bg-[#6ba396] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Download className="w-5 h-5" />
              <span>{isDownloading ? "Generating..." : "Download PDF"}</span>
            </motion.button>
          </div>
        </div>
      </motion.div>

      {/* Appointment Form Modal */}
      <AnimatePresence>
        {showAppointmentForm && editingAppointment && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            >
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-gray-900">
                    {editingAppointment.id
                      ? "Edit Appointment"
                      : "Add New Appointment"}
                  </h2>
                  <button
                    onClick={() => {
                      setEditingAppointment(null);
                      setShowAppointmentForm(false);
                    }}
                    className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>

              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Doctor Name *
                    </label>
                    <input
                      type="text"
                      value={editingAppointment.doctorName || ""}
                      onChange={(e) =>
                        setEditingAppointment((prev) => ({
                          ...prev,
                          doctorName: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      placeholder="Dr. John Smith"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Specialty *
                    </label>
                    <input
                      type="text"
                      value={editingAppointment.specialty || ""}
                      onChange={(e) =>
                        setEditingAppointment((prev) => ({
                          ...prev,
                          specialty: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      placeholder="Cardiologist"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Date *
                    </label>
                    <input
                      type="date"
                      value={editingAppointment.date || ""}
                      onChange={(e) =>
                        setEditingAppointment((prev) => ({
                          ...prev,
                          date: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Time *
                    </label>
                    <input
                      type="time"
                      value={editingAppointment.time || ""}
                      onChange={(e) =>
                        setEditingAppointment((prev) => ({
                          ...prev,
                          time: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Type *
                    </label>
                    <select
                      value={editingAppointment.type || ""}
                      onChange={(e) =>
                        setEditingAppointment((prev) => ({
                          ...prev,
                          type: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                    >
                      <option value="">Select type</option>
                      <option value="Consultation">Consultation</option>
                      <option value="Follow-up">Follow-up</option>
                      <option value="Annual Physical">Annual Physical</option>
                      <option value="Specialist Visit">Specialist Visit</option>
                      <option value="Emergency">Emergency</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Location
                    </label>
                    <input
                      type="text"
                      value={editingAppointment.location || ""}
                      onChange={(e) =>
                        setEditingAppointment((prev) => ({
                          ...prev,
                          location: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      placeholder="Medical Center, 123 Main St."
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Notes
                    </label>
                    <textarea
                      value={editingAppointment.notes || ""}
                      onChange={(e) =>
                        setEditingAppointment((prev) => ({
                          ...prev,
                          notes: e.target.value,
                        }))
                      }
                      rows={3}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
                      placeholder="Additional notes or instructions..."
                    />
                  </div>
                </div>

                <div className="flex space-x-3 mt-6">
                  <button
                    onClick={() => {
                      setEditingAppointment(null);
                      setShowAppointmentForm(false);
                    }}
                    className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={handleAppointmentSave}
                    className="flex-1 flex items-center justify-center space-x-2 bg-[#76B3A8] text-white px-6 py-3 rounded-lg hover:bg-[#6ba396] transition-colors"
                  >
                    <Save className="w-4 h-4" />
                    <span>Save Appointment</span>
                  </motion.button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
