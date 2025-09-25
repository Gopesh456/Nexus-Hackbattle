import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Heart, Lock, User } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export const Login: React.FC = () => {
  const [formData, setFormData] = useState({ user: '', password: '' });
  const [error, setError] = useState('');
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await login(formData.user, formData.password);
      navigate('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-gray-50 flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-md w-full"
      >
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="inline-flex items-center justify-center w-16 h-16 bg-[#76B3A8] rounded-full mb-4"
            >
              <Heart className="w-8 h-8 text-white" />
            </motion.div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Welcome Back</h1>
            <p className="text-[#7D7F7C]">Sign in to your health journey</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#7D7F7C] w-5 h-5" />
                <input
                  type="text"
                  required
                  value={formData.user}
                  onChange={(e) => setFormData({ ...formData, user: e.target.value })}
                  className="w-full pl-11 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
                  placeholder="Enter your username"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#7D7F7C] w-5 h-5" />
                <input
                  type="password"
                  required
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full pl-11 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76B3A8] focus:border-transparent transition-all duration-200"
                  placeholder="Enter your password"
                />
              </div>
            </div>

            {error && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="text-red-500 text-sm bg-red-50 p-3 rounded-lg"
              >
                {error}
              </motion.div>
            )}

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={isLoading}
              className="w-full bg-[#76B3A8] text-white py-3 rounded-lg font-semibold hover:bg-[#6BA399] transition-colors duration-200 disabled:opacity-50"
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </motion.button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-[#7D7F7C]">
              Don't have an account?{' '}
              <Link
                to="/register"
                className="text-[#76B3A8] hover:text-[#6BA399] font-semibold transition-colors duration-200"
              >
                Sign up
              </Link>
            </p>
          </div>

          <div className="mt-4 text-center text-sm text-[#7D7F7C]">
            <p>Demo credentials: admin / password</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};