import React, { useState } from "react";
import { motion } from "framer-motion";
import { Bot, Send, Mic, MicOff } from "lucide-react";

export const NurseAgentPage: React.FC = () => {
  const [message, setMessage] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      content:
        "Hello! I'm your virtual nurse assistant. How can I help you today?",
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);

  const handleSendMessage = () => {
    if (message.trim()) {
      const newMessage = {
        id: messages.length + 1,
        type: "user",
        content: message,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages([...messages, newMessage]);
      setMessage("");

      // Simulate bot response
      setTimeout(() => {
        const botResponse = {
          id: messages.length + 2,
          type: "bot",
          content:
            "Thank you for your message. I'm processing your request and will provide you with appropriate health guidance.",
          timestamp: new Date().toLocaleTimeString(),
        };
        setMessages((prev) => [...prev, botResponse]);
      }, 1000);
    }
  };

  return (
    <div className="h-full flex flex-col p-6">
      {/* Page Header */}
      <div className="mb-6">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center space-x-3 mb-2"
        >
          <Bot className="w-8 h-8 text-[#76B3A8]" />
          <h1 className="text-3xl font-bold text-gray-900">
            AI Nurse Assistant
          </h1>
        </motion.div>
        <p className="text-gray-600">
          Get personalized health advice and support
        </p>
      </div>

      {/* Chat Interface */}
      <div className="flex-1 bg-white rounded-xl border border-gray-200 flex flex-col">
        {/* Chat Messages */}
        <div className="flex-1 p-6 overflow-y-auto">
          <div className="space-y-4">
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${
                  msg.type === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    msg.type === "user"
                      ? "bg-[#76B3A8] text-white"
                      : "bg-gray-100 text-gray-900"
                  }`}
                >
                  <p className="text-sm">{msg.content}</p>
                  <p
                    className={`text-xs mt-1 ${
                      msg.type === "user" ? "text-white/70" : "text-gray-500"
                    }`}
                  >
                    {msg.timestamp}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Chat Input */}
        <div className="border-t border-gray-200 p-4">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setIsListening(!isListening)}
              className={`p-2 rounded-full ${
                isListening
                  ? "bg-red-100 text-red-600"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              } transition-all`}
            >
              {isListening ? (
                <MicOff className="w-5 h-5" />
              ) : (
                <Mic className="w-5 h-5" />
              )}
            </button>

            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              placeholder="Ask me about your health..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent"
            />

            <button
              onClick={handleSendMessage}
              disabled={!message.trim()}
              className="p-2 bg-[#76B3A8] text-white rounded-full hover:bg-[#6ba396] disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
        <button className="p-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-all text-sm">
          Symptom Checker
        </button>
        <button className="p-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-all text-sm">
          Medication Info
        </button>
        <button className="p-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-all text-sm">
          Health Tips
        </button>
        <button className="p-3 bg-orange-50 text-orange-700 rounded-lg hover:bg-orange-100 transition-all text-sm">
          Emergency Help
        </button>
      </div>
    </div>
  );
};
