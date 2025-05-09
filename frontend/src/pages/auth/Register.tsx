import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useMutation } from 'react-query';
import { api } from '../../services/api';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';

interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  password2: string;
  first_name: string;
  last_name: string;
}

const Register: React.FC = () => {
  const navigate = useNavigate();
  const [registerError, setRegisterError] = useState<string | null>(null);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<RegisterFormData>();
  
  const password = watch('password');
  
  const mutation = useMutation(
    (data: RegisterFormData) => {
      return api.post('/users/register/', data);
    },
    {
      onSuccess: () => {
        navigate('/auth/login', {
          state: { message: 'Registration successful! You can now log in.' },
        });
      },
      onError: (error: any) => {
        if (error.response?.data) {
          // Format validation errors
          const errorData = error.response.data;
          const errorMessages = [];
          
          for (const key in errorData) {
            if (Array.isArray(errorData[key])) {
              errorMessages.push(`${key}: ${errorData[key].join(', ')}`);
            } else if (typeof errorData[key] === 'string') {
              errorMessages.push(`${key}: ${errorData[key]}`);
            }
          }
          
          setRegisterError(errorMessages.join('\n'));
        } else {
          setRegisterError('Registration failed. Please try again.');
        }
      },
    }
  );
  
  const onSubmit = (data: RegisterFormData) => {
    setRegisterError(null);
    mutation.mutate(data);
  };
  
  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Create your account</h2>
      
      {registerError && (
        <div className="mb-4 p-3 bg-red-100 text-red-800 rounded-md whitespace-pre-line">
          {registerError}
        </div>
      )}
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label
              htmlFor="first_name"
              className="block text-sm font-medium text-gray-700"
            >
              First Name
            </label>
            <Input
              id="first_name"
              type="text"
              {...register('first_name', {
                required: 'First name is required',
              })}
              className="mt-1"
            />
            {errors.first_name && (
              <p className="mt-1 text-sm text-red-600">{errors.first_name.message}</p>
            )}
          </div>
          
          <div>
            <label
              htmlFor="last_name"
              className="block text-sm font-medium text-gray-700"
            >
              Last Name
            </label>
            <Input
              id="last_name"
              type="text"
              {...register('last_name', {
                required: 'Last name is required',
              })}
              className="mt-1"
            />
            {errors.last_name && (
              <p className="mt-1 text-sm text-red-600">{errors.last_name.message}</p>
            )}
          </div>
        </div>
        
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
              minLength: {
                value: 3,
                message: 'Username must be at least 3 characters',
              },
            })}
            className="mt-1"
          />
          {errors.username && (
            <p className="mt-1 text-sm text-red-600">{errors.username.message}</p>
          )}
        </div>
        
        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700"
          >
            Email
          </label>
          <Input
            id="email"
            type="email"
            {...register('email', {
              required: 'Email is required',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Invalid email address',
              },
            })}
            className="mt-1"
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
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
              minLength: {
                value: 8,
                message: 'Password must be at least 8 characters',
              },
            })}
            className="mt-1"
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
          )}
        </div>
        
        <div>
          <label
            htmlFor="password2"
            className="block text-sm font-medium text-gray-700"
          >
            Confirm Password
          </label>
          <Input
            id="password2"
            type="password"
            {...register('password2', {
              required: 'Please confirm your password',
              validate: (value) =>
                value === password || 'The passwords do not match',
            })}
            className="mt-1"
          />
          {errors.password2 && (
            <p className="mt-1 text-sm text-red-600">{errors.password2.message}</p>
          )}
        </div>
        
        <div>
          <Button type="submit" className="w-full" isLoading={mutation.isLoading}>
            Sign up
          </Button>
        </div>
      </form>
      
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Already have an account?{' '}
          <Link to="/auth/login" className="text-primary-700 hover:text-primary-800">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
