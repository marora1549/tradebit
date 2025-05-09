import jwtDecode from 'jwt-decode';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
const TOKEN_KEY = process.env.REACT_APP_TOKEN_KEY || 'tradebit_auth_token';
const REFRESH_TOKEN_KEY = process.env.REACT_APP_REFRESH_TOKEN_KEY || 'tradebit_refresh_token';

interface DecodedToken {
  exp: number;
  user_id: string;
  username: string;
  [key: string]: any;
}

/**
 * Check if token is expired
 */
export const isTokenExpired = (token: string): boolean => {
  try {
    const decoded = jwtDecode<DecodedToken>(token);
    return decoded.exp * 1000 < Date.now();
  } catch (e) {
    return true;
  }
};

/**
 * Get user from token
 */
export const getUserFromToken = (token: string): any => {
  try {
    const decoded = jwtDecode<DecodedToken>(token);
    return {
      id: decoded.user_id,
      username: decoded.username,
    };
  } catch (e) {
    return null;
  }
};

/**
 * Refresh access token
 */
export const refreshToken = async (): Promise<string | null> => {
  const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
  
  if (!refreshToken) {
    return null;
  }
  
  try {
    const response = await axios.post(`${API_URL}/token/refresh/`, {
      refresh: refreshToken,
    });
    
    const { access } = response.data;
    localStorage.setItem(TOKEN_KEY, access);
    
    return access;
  } catch (error) {
    // If refresh fails, clear tokens
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    return null;
  }
};
