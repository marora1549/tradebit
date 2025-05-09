import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './stores/authStore';

// Layouts
import DashboardLayout from './layouts/DashboardLayout';
import AuthLayout from './layouts/AuthLayout';

// Pages
import Dashboard from './pages/Dashboard';
import Portfolio from './pages/Portfolio';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Settings from './pages/Settings';
import ZerodhaIntegration from './pages/ZerodhaIntegration';
import NotFound from './pages/NotFound';

// Protected Route Component
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuthStore();
  
  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }
  
  return <>{children}</>;
};

function App() {
  const { checkAuth } = useAuthStore();
  
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);
  
  return (
    <Routes>
      {/* Auth Routes */}
      <Route path="/auth" element={<AuthLayout />}>
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route index element={<Navigate to="/auth/login" replace />} />
      </Route>
      
      {/* Dashboard Routes */}
      <Route 
        path="/" 
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="portfolio" element={<Portfolio />} />
        <Route path="settings" element={<Settings />} />
        <Route path="zerodha" element={<ZerodhaIntegration />} />
      </Route>
      
      {/* Not Found */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;
