import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useMutation } from 'react-query';
import { api } from '../../services/api';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '../ui/Card';

interface ZerodhaCredentialsFormData {
  api_key: string;
  api_secret: string;
}

const ZerodhaSettingsForm: React.FC = () => {
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ZerodhaCredentialsFormData>();
  
  const mutation = useMutation(
    (data: ZerodhaCredentialsFormData) => {
      return api.post('/users/zerodha-credentials/', data);
    },
    {
      onSuccess: () => {
        setSuccessMessage('Zerodha credentials updated successfully.');
        setErrorMessage(null);
        reset();
        
        // Clear success message after 5 seconds
        setTimeout(() => {
          setSuccessMessage(null);
        }, 5000);
      },
      onError: (error: any) => {
        setErrorMessage(
          error.response?.data?.message ||
          'Failed to update Zerodha credentials. Please try again.'
        );
        setSuccessMessage(null);
      },
    }
  );
  
  const onSubmit = (data: ZerodhaCredentialsFormData) => {
    mutation.mutate(data);
  };
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Zerodha API Credentials</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit(onSubmit)}>
        <CardContent className="space-y-4">
          {successMessage && (
            <div className="p-3 bg-green-100 text-green-800 rounded-md">
              {successMessage}
            </div>
          )}
          
          {errorMessage && (
            <div className="p-3 bg-red-100 text-red-800 rounded-md">
              {errorMessage}
            </div>
          )}
          
          <div className="space-y-2">
            <label htmlFor="api_key" className="text-sm font-medium">
              API Key
            </label>
            <Input
              id="api_key"
              type="text"
              {...register('api_key', { required: 'API Key is required' })}
              placeholder="Enter your Zerodha API Key"
            />
            {errors.api_key && (
              <p className="text-sm text-red-500">{errors.api_key.message}</p>
            )}
          </div>
          
          <div className="space-y-2">
            <label htmlFor="api_secret" className="text-sm font-medium">
              API Secret
            </label>
            <Input
              id="api_secret"
              type="password"
              {...register('api_secret', { required: 'API Secret is required' })}
              placeholder="Enter your Zerodha API Secret"
            />
            {errors.api_secret && (
              <p className="text-sm text-red-500">{errors.api_secret.message}</p>
            )}
          </div>
          
          <div className="pt-2">
            <p className="text-sm text-gray-500">
              Enter your Zerodha API credentials to enable integration with your Zerodha account.
              You can find these credentials in your Zerodha Developer Console.
            </p>
          </div>
        </CardContent>
        
        <CardFooter>
          <Button type="submit" isLoading={mutation.isLoading}>
            Save Credentials
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
};

export default ZerodhaSettingsForm;
