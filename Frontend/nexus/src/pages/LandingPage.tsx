import React, { useEffect, useRef } from "react";
import { motion, useAnimation, useInView } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
  Heart,
  Activity,
  Pill,
  Utensils,
  FlaskConical,
  Bot,
  Shield,
  Stethoscope,
  FileText,
  CheckCircle,
  Star,
  ArrowRight,
  Smartphone,
  Brain,
  Users,
} from "lucide-react";

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  // Animation controls
  const heroControls = useAnimation();
  const featuresControls = useAnimation();
  const agentsControls = useAnimation();

  // Refs for intersection observer
  const heroRef = useRef(null);
  const featuresRef = useRef(null);
  const agentsRef = useRef(null);

  // Track visibility
  const heroInView = useInView(heroRef, { once: true });
  const featuresInView = useInView(featuresRef, { once: true });
  const agentsInView = useInView(agentsRef, { once: true });

  // Trigger animations when sections come into view
  useEffect(() => {
    if (heroInView) {
      heroControls.start("visible");
    }
  }, [heroControls, heroInView]);

  useEffect(() => {
    if (featuresInView) {
      featuresControls.start("visible");
    }
  }, [featuresControls, featuresInView]);

  useEffect(() => {
    if (agentsInView) {
      agentsControls.start("visible");
    }
  }, [agentsControls, agentsInView]);

  const features = [
    {
      icon: <Stethoscope className="w-8 h-8" />,
      title: "Symptom Checking & Appointments",
      description:
        "AI-powered symptom analysis and seamless appointment booking with healthcare providers.",
    },
    {
      icon: <Heart className="w-8 h-8" />,
      title: "Health Profile Management",
      description:
        "Comprehensive health profiles with medical history, allergies, and vital statistics tracking.",
    },
    {
      icon: <FlaskConical className="w-8 h-8" />,
      title: "Lab Report Tracking",
      description:
        "Upload, organize, and track your lab results with intelligent insights and trend analysis.",
    },
    {
      icon: <Pill className="w-8 h-8" />,
      title: "Medication Management",
      description:
        "Smart medication reminders, dosage tracking, and drug interaction monitoring.",
    },
    {
      icon: <Utensils className="w-8 h-8" />,
      title: "Nutrition & Food Logging",
      description:
        "Track your meals, monitor nutrition goals, and receive personalized dietary recommendations.",
    },
    {
      icon: <Activity className="w-8 h-8" />,
      title: "Real-time Fitness Tracking",
      description:
        "Connect with wearables for continuous health monitoring and activity analysis.",
    },
  ];

  const agents = [
    {
      icon: <Bot className="w-12 h-12" />,
      name: "Nurse Agent",
      description:
        "Interacts with users via chat to get symptoms and health data, automatically books appointments using Twilio and Deepgram speech recognition.",
      color: "from-purple-500 to-purple-600",
    },
    {
      icon: <Pill className="w-12 h-12" />,
      name: "Med Agent",
      description:
        "Assists with medication reminders, tracking adherence, managing complex prescription schedules, and automatically restocks medications on given dates using browser-use technology.",
      color: "from-blue-500 to-blue-600",
    },
    {
      icon: <Shield className="w-12 h-12" />,
      name: "Guardian Agent",
      description:
        "Provides continuous health monitoring, detects anomalies, and sends emergency alerts when needed.",
      color: "from-red-500 to-red-600",
    },
    {
      icon: <FileText className="w-12 h-12" />,
      name: "Lab Report Agent",
      description:
        "Manages user lab reports, provides historical analysis, and delivers actionable health insights.",
      color: "from-green-500 to-green-600",
    },
  ];

  const testimonials = [];

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation Header */}
      <nav className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-sm border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-[#76B3A8] to-[#5A9B8E] rounded-xl flex items-center justify-center">
                <Heart className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Nexus</h1>
                <p className="text-xs text-gray-500">Health Platform</p>
              </div>
            </div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              <a
                href="#features"
                className="text-gray-600 hover:text-[#76B3A8] transition-colors"
              >
                Features
              </a>
              <a
                href="#agents"
                className="text-gray-600 hover:text-[#76B3A8] transition-colors"
              >
                AI Agents
              </a>
              <a
                href="#about"
                className="text-gray-600 hover:text-[#76B3A8] transition-colors"
              >
                About
              </a>
            </div>

            {/* Auth Buttons */}
            <div className="flex items-center space-x-3">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate("/login")}
                className="px-4 py-2 text-[#76B3A8] border border-[#76B3A8] rounded-lg hover:bg-[#76B3A8] hover:text-white transition-all duration-200"
              >
                Login
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate("/register")}
                className="px-4 py-2 bg-[#76B3A8] text-white rounded-lg hover:bg-[#6ba396] transition-all duration-200"
              >
                Register
              </motion.button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section
        ref={heroRef}
        className="pt-24 pb-20 bg-gradient-to-br from-gray-50 to-white relative overflow-hidden"
      >
        {/* Background Decorations */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-20 right-20 w-64 h-64 bg-[#76B3A8]/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 left-20 w-96 h-96 bg-[#76B3A8]/5 rounded-full blur-3xl"></div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Hero Content */}
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={heroControls}
              variants={{
                visible: {
                  opacity: 1,
                  y: 0,
                  transition: { duration: 0.8, ease: "easeOut" },
                },
              }}
              className="space-y-8"
            >
              <div className="space-y-4">
                <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                  Your Health,{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#76B3A8] to-[#5A9B8E]">
                    Intelligently
                  </span>{" "}
                  Managed
                </h1>
                <p className="text-xl text-gray-600 leading-relaxed">
                  Empower yourself to monitor and manage your health seamlessly
                  with AI-powered agents. Get intelligent health assistance,
                  easy access to your data, and proactive care—all in one place.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => navigate("/register")}
                  className="flex items-center justify-center space-x-2 px-8 py-4 bg-[#76B3A8] text-white rounded-xl hover:bg-[#6ba396] transition-all duration-200 text-lg font-semibold"
                >
                  <span>Get Started Free</span>
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => navigate("/login")}
                  className="flex items-center justify-center space-x-2 px-8 py-4 border-2 border-[#76B3A8] text-[#76B3A8] rounded-xl hover:bg-[#76B3A8] hover:text-white transition-all duration-200 text-lg font-semibold"
                >
                  <span>Sign In</span>
                </motion.button>
              </div>

              {/* Trust Indicators */}
              <div className="flex items-center space-x-6 text-sm text-gray-500">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>Ambient Gaurd</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Shield className="w-5 h-5 text-blue-500" />
                  <span>Secure & Private</span>
                </div>
              </div>
            </motion.div>

            {/* Hero Visual */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={heroControls}
              variants={{
                visible: {
                  opacity: 1,
                  x: 0,
                  transition: { duration: 0.8, delay: 0.2, ease: "easeOut" },
                },
              }}
              className="relative"
            >
              <div className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
                <div className="space-y-6">
                  {/* Mock Chat Interface */}
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-[#76B3A8] to-[#5A9B8E] rounded-full flex items-center justify-center">
                        <Bot className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          Nurse Agent
                        </p>
                        <p className="text-xs text-gray-500">
                          AI Health Assistant
                        </p>
                      </div>
                    </div>
                    <div className="bg-[#76B3A8]/10 rounded-lg p-4">
                      <p className="text-sm text-gray-700">
                        Hi! I've noticed some unusual patterns in your health
                        data. Would you like me to schedule a check-up with Dr.
                        Smith?
                      </p>
                    </div>
                  </div>

                  {/* Mock Health Metrics */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-green-50 rounded-lg p-4 text-center">
                      <Heart className="w-8 h-8 text-green-600 mx-auto mb-2" />
                      <p className="text-sm font-medium text-gray-900">
                        Heart Rate
                      </p>
                      <p className="text-lg font-bold text-green-600">72 BPM</p>
                    </div>
                    <div className="bg-blue-50 rounded-lg p-4 text-center">
                      <Activity className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                      <p className="text-sm font-medium text-gray-900">Steps</p>
                      <p className="text-lg font-bold text-blue-600">8,432</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating Elements */}
              <motion.div
                animate={{ y: [-10, 10, -10] }}
                transition={{
                  repeat: Infinity,
                  duration: 4,
                  ease: "easeInOut",
                }}
                className="absolute -top-4 -right-4 w-20 h-20 bg-gradient-to-r from-purple-400 to-purple-500 rounded-full flex items-center justify-center shadow-lg"
              >
                <Smartphone className="w-10 h-10 text-white" />
              </motion.div>

              <motion.div
                animate={{ y: [10, -10, 10] }}
                transition={{
                  repeat: Infinity,
                  duration: 3,
                  ease: "easeInOut",
                }}
                className="absolute -bottom-4 -left-4 w-16 h-16 bg-gradient-to-r from-green-400 to-green-500 rounded-full flex items-center justify-center shadow-lg"
              >
                <Brain className="w-8 h-8 text-white" />
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" ref={featuresRef} className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={featuresControls}
            variants={{
              visible: { opacity: 1, y: 0, transition: { duration: 0.8 } },
            }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Everything You Need for Better Health
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our comprehensive platform combines cutting-edge AI with intuitive
              design to give you complete control over your health journey.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={featuresControls}
                variants={{
                  visible: {
                    opacity: 1,
                    y: 0,
                    transition: {
                      duration: 0.6,
                      delay: index * 0.1,
                    },
                  },
                }}
                whileHover={{ y: -5, transition: { duration: 0.2 } }}
                className="bg-white border border-gray-200 rounded-xl p-8 shadow-sm hover:shadow-lg transition-all duration-300"
              >
                <div className="w-16 h-16 bg-gradient-to-r from-[#76B3A8] to-[#5A9B8E] rounded-xl flex items-center justify-center mb-6 text-white">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Agents Section */}
      <section id="agents" ref={agentsRef} className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={agentsControls}
            variants={{
              visible: { opacity: 1, y: 0, transition: { duration: 0.8 } },
            }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Meet Your AI Health Team
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our intelligent agents work around the clock to provide
              personalized health assistance, monitoring, and support tailored
              to your unique needs.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-8">
            {agents.map((agent, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={agentsControls}
                variants={{
                  visible: {
                    opacity: 1,
                    scale: 1,
                    transition: {
                      duration: 0.6,
                      delay: index * 0.15,
                    },
                  },
                }}
                whileHover={{ scale: 1.02, transition: { duration: 0.2 } }}
                className="bg-white rounded-xl p-8 shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-200"
              >
                <div className="flex items-start space-x-4">
                  <div
                    className={`w-16 h-16 bg-gradient-to-r ${agent.color} rounded-xl flex items-center justify-center text-white flex-shrink-0`}
                  >
                    {agent.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">
                      {agent.name}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {agent.description}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Trusted by Patients and Providers
            </h2>
            <p className="text-xl text-gray-600">
              See what our users are saying about their experience with Nexus
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-gray-50 rounded-xl p-6 border border-gray-200"
              >
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star
                      key={i}
                      className="w-5 h-5 text-yellow-400 fill-current"
                    />
                  ))}
                </div>
                <blockquote className="text-gray-700 mb-4 italic">
                  "{testimonial.quote}"
                </blockquote>
                <cite className="text-sm font-medium text-gray-900">
                  {testimonial.author}
                </cite>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-20 bg-gradient-to-r from-[#76B3A8] to-[#5A9B8E]">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="space-y-8"
          >
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to Transform Your Health Journey?
            </h2>
            <p className="text-xl text-white/90 mb-8">
              Join thousands of users who are already managing their health
              smarter with Nexus
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate("/register")}
                className="px-8 py-4 bg-white text-[#76B3A8] rounded-xl hover:bg-gray-50 transition-all duration-200 text-lg font-semibold"
              >
                Start Your Free Trial
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate("/login")}
                className="px-8 py-4 border-2 border-white text-white rounded-xl hover:bg-white hover:text-[#76B3A8] transition-all duration-200 text-lg font-semibold"
              >
                Sign In Now
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-[#76B3A8] to-[#5A9B8E] rounded-xl flex items-center justify-center">
                  <Heart className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-bold">Nexus</h3>
                  <p className="text-sm text-gray-400">Health Platform</p>
                </div>
              </div>
              <p className="text-gray-400">
                Empowering individuals to take control of their health with
                intelligent AI assistance.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Platform</h4>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <a
                    href="#features"
                    className="hover:text-white transition-colors"
                  >
                    Features
                  </a>
                </li>
                <li>
                  <a
                    href="#agents"
                    className="hover:text-white transition-colors"
                  >
                    AI Agents
                  </a>
                </li>
                <li></li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Security
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2025 Nexus Health Platform. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};
