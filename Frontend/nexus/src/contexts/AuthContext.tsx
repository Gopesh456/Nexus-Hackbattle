import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import Cookies from "js-cookie";
import { AuthContextType, User } from "../types";
import { apiClient } from "../utils/api";

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = Cookies.get("token");
    if (token) {
      // In a real app, validate token with API
      setUser({ id: "1", user: "demo_user" });
    }
    setIsLoading(false);
  }, []);

  const login = async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await apiClient.login(username, password);

      // Check for successful login response
      if (response.message === "Login successful" && response.tokens) {
        // Set user state - token is already stored in cookie by apiClient.login
        setUser({
          id: response.user.id.toString(),
          user: response.user.username,
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await apiClient.register(username, password);

      // Check for successful registration
      if (
        response.message === "User registered successfully" &&
        response.tokens
      ) {
        // Set user state - token is already stored in cookie by apiClient.register
        setUser({
          id: response.user.id.toString(),
          user: response.user.username,
        });
      }

      return response;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    await apiClient.logout();
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    isLoading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
