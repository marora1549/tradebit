import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

const AuthLayout: React.FC = () => {
  const { isAuthenticated } = useAuthStore();
  
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gray-50 py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="text-center text-3xl font-extrabold text-gray-900">
          TradeBit
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Personal Stock Portfolio Management System
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
