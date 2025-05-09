import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from 'react-query';
import { api } from '../services/api';
import { Button } from '../components/ui/Button';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '../ui/Card';

const ZerodhaIntegration: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [statusMessage, setStatusMessage] = useState<string>('');
  
  // Extract request token from URL if present (after redirect from Zerodha)
  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const requestToken = searchParams.get('request_token');
    
    if (requestToken) {
      // Handle Zerodha callback with request token
      setStatus('loading');
      setStatusMessage('Processing authentication response from Zerodha...');
      
      api.get(`/zerodha/callback/?request_token=${requestToken}`)
        .then(() => {
          setStatus('success');
          setStatusMessage('Zerodha authentication successful!');
          
          // Clear the request token from URL
          navigate('/zerodha', { replace: true });
        })
        .catch((error) => {
          setStatus('error');
          setStatusMessage(
            error.response?.data?.error ||
            'Failed to authenticate with Zerodha. Please try again.'
          );
        });
    }
  }, [location.search, navigate]);
  
  // Get login URL for Zerodha
  const { data: loginUrlData, isLoading: isLoadingLoginUrl } = useQuery<{ login_url: string }>(
    'zerodhaLoginUrl',
    async () => {
      const response = await api.get('/zerodha/login/');
      return response.data;
    },
    {
      enabled: status === 'idle',
      retry: false,
      onError: () => {
        setStatus('error');
        setStatusMessage('Failed to get Zerodha login URL. Please check your API credentials in Settings.');
      }
    }
  );
  
  // For syncing holdings
  const syncHoldingsMutation = useMutation(
    () => api.post('/zerodha/sync-holdings/'),
    {
      onSuccess: (response) => {
        const { created, updated, total } = response.data;
        setStatus('success');
        setStatusMessage(`Holdings synced successfully! Created: ${created}, Updated: ${updated}, Total: ${total}`);
      },
      onError: (error: any) => {
        setStatus('error');
        setStatusMessage(
          error.response?.data?.message ||
          'Failed to sync holdings. Please check your Zerodha connection.'
        );
      },
    }
  );
  
  const handleLogin = () => {
    if (loginUrlData?.login_url) {
      window.location.href = loginUrlData.login_url;
    }
  };
  
  const handleSyncHoldings = () => {
    setStatus('loading');
    setStatusMessage('Syncing holdings from Zerodha...');
    syncHoldingsMutation.mutate();
  };
  
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Zerodha Integration</h1>
      
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Connect with Zerodha</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600 mb-4">
            Connect your Zerodha account to automatically import your holdings and track your investments.
          </p>
          
          {status === 'loading' && (
            <div className="p-4 bg-blue-50 text-blue-700 rounded-md mb-4">
              <div className="flex items-center">
                <div className="mr-3 animate-spin rounded-full h-5 w-5 border-b-2 border-blue-700"></div>
                <p>{statusMessage}</p>
              </div>
            </div>
          )}
          
          {status === 'success' && (
            <div className="p-4 bg-green-50 text-green-700 rounded-md mb-4">
              <p>{statusMessage}</p>
            </div>
          )}
          
          {status === 'error' && (
            <div className="p-4 bg-red-50 text-red-700 rounded-md mb-4">
              <p>{statusMessage}</p>
            </div>
          )}
        </CardContent>
        <CardFooter className="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-2">
          <Button
            onClick={handleLogin}
            isLoading={isLoadingLoginUrl}
            disabled={status === 'loading'}
          >
            Connect with Zerodha
          </Button>
          
          <Button
            variant="outline"
            onClick={handleSyncHoldings}
            isLoading={syncHoldingsMutation.isLoading}
            disabled={status === 'loading'}
          >
            Sync Holdings
          </Button>
        </CardFooter>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Zerodha Integration Guide</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium">Step 1: Set Up API Credentials</h3>
              <p className="text-gray-600">
                First, go to the Settings page and enter your Zerodha API Key and Secret.
                You can obtain these from the Zerodha Developer Console.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium">Step 2: Connect Your Account</h3>
              <p className="text-gray-600">
                Click the "Connect with Zerodha" button above and complete the authorization
                process on the Zerodha website.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium">Step 3: Sync Your Holdings</h3>
              <p className="text-gray-600">
                After connecting, click "Sync Holdings" to import your holdings from Zerodha
                into TradeBit. You can sync any time to update your portfolio with the latest data.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ZerodhaIntegration;
