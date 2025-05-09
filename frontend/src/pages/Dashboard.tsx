import React from 'react';
import PortfolioSummary from '../components/Dashboard/PortfolioSummary';

const Dashboard: React.FC = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <PortfolioSummary />
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Placeholder for additional dashboard widgets */}
        {/* These will be implemented in future phases */}
      </div>
    </div>
  );
};

export default Dashboard;
