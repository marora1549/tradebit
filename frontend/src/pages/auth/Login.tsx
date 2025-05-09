import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useMutation } from 'react-query';
import { useAuthStore } from '../../stores/authStore';
import { api } from '../../services/api';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';

interface LoginFormData {
  username: string;
  password: string;
}

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuthStore();
  const [loginError, setLoginError] = useState<string | null>(null);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>();
  
  const mutation = useMutation(
    (data: LoginFormData) => {
      return api.post('/token/', data);
    },
    {
      onSuccess: (response) => {
        const { access, refresh } = response.data;
        login(access, refresh);
        navigate('/');
      },
      onError: (error: any) => {
        setLoginError(
          error.response?.data?.detail ||
          'Login failed. Please check your credentials.'
        );
      },
    }
  );
  
  const onSubmit = (data: LoginFormData) => {
    setLoginError(null);
    mutation.mutate(data);
  };
  
  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Sign in to your account</h2>
      
      {loginError && (
        <div className="mb-4 p-3 bg-red-100 text-red-800 rounded-md">
          {loginError}
        </div>
      )}
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div>
          <label
            htmlFor="username"
            className="block text-sm font-medium text-gray-700"
          >
            Username
          </label>
          <Input
            id="username"
            type="text"
            {...register('username', {
              required: 'Username is required',
            })}
            className="mt-1"
          />
          {errors.username && (
            <p className="mt-1 text-sm text-red-600">{errors.username.message}</p>
          )}
        </div>
        
        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-700"
          >
            Password
          </label>
          <Input
            id="password"
            type="password"
            {...register('password', {
              required: 'Password is required',
            })}
            className="mt-1"
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
          )}
        </div>
        
        <div>
          <Button type="submit" className="w-full" isLoading={mutation.isLoading}>
            Sign in
          </Button>
        </div>
      </form>
      
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Don't have an account?{' '}
          <Link to="/auth/register" className="text-primary-700 hover:text-primary-800">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
