import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';

const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full text-center">
        <h1 className="text-6xl font-bold text-primary-700">404</h1>
        <h2 className="mt-4 text-2xl font-bold text-gray-900">Page Not Found</h2>
        <p className="mt-2 text-gray-600">
          The page you are looking for doesn't exist or has been moved.
        </p>
        <div className="mt-6">
          <Link to="/">
            <Button>Go to Dashboard</Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
