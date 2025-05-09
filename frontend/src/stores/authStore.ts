import { create } from 'zustand';
import { isTokenExpired, getUserFromToken, refreshToken } from '../services/auth';

const TOKEN_KEY = process.env.REACT_APP_TOKEN_KEY || 'tradebit_auth_token';
const REFRESH_TOKEN_KEY = process.env.REACT_APP_REFRESH_TOKEN_KEY || 'tradebit_refresh_token';

interface User {
  id: string;
  username: string;
  [key: string]: any;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  login: (accessToken: string, refreshToken: string) => void;
  logout: () => void;
  checkAuth: () => Promise<boolean>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  isAuthenticated: false,
  user: null,
  
  login: (accessToken, refreshToken) => {
    localStorage.setItem(TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
    
    const user = getUserFromToken(accessToken);
    
    set({
      isAuthenticated: true,
      user,
    });
  },
  
  logout: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    
    set({
      isAuthenticated: false,
      user: null,
    });
  },
  
  checkAuth: async () => {
    const token = localStorage.getItem(TOKEN_KEY);
    
    if (!token) {
      get().logout();
      return false;
    }
    
    if (isTokenExpired(token)) {
      const newToken = await refreshToken();
      
      if (!newToken) {
        get().logout();
        return false;
      }
      
      const user = getUserFromToken(newToken);
      
      set({
        isAuthenticated: true,
        user,
      });
      
      return true;
    }
    
    const user = getUserFromToken(token);
    
    set({
      isAuthenticated: true,
      user,
    });
    
    return true;
  },
}));
