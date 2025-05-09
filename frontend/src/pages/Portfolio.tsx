import React from 'react';
import HoldingsList from '../components/Portfolio/HoldingsList';

const Portfolio: React.FC = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Portfolio</h1>
      <HoldingsList />
    </div>
  );
};

export default Portfolio;
