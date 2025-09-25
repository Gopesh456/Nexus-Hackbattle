import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import Cookies from "js-cookie";
import { AuthContextType, User, RegisterResponse } from "../types";
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
      const response = await apiClient.post("login/", {
        username: username,
        password: password,
      });

      if (response.tokens?.access) {
        Cookies.set("token", response.tokens.access, { expires: 7 });
        setUser({
          id: response.user?.id?.toString() || "1",
          user: response.user?.username || username,
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (
    username: string,
    password: string
  ): Promise<RegisterResponse> => {
    setIsLoading(true);
    try {
      const response: RegisterResponse = await apiClient.post("register/", {
        username: username,
        password: password,
      });

      // Check for successful registration
      if (
        response.message === "User registered successfully" &&
        response.tokens
      ) {
        // Handle both token formats: string or object with access property
        const token =
          typeof response.tokens === "string"
            ? response.tokens
            : response.tokens.access;

        if (token && token !== "") {
          Cookies.set("token", token, { expires: 7 });
          setUser({
            id: response.user_id?.toString() || "1",
            user: username,
          });
        }
      }

      return response;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    Cookies.remove("token");
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
