import React from 'react';
import ZerodhaSettingsForm from '../components/Settings/ZerodhaSettingsForm';

const Settings: React.FC = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Settings</h1>
      
      <div className="space-y-6">
        <ZerodhaSettingsForm />
        
        {/* Future settings components will be added here */}
      </div>
    </div>
  );
};

export default Settings;
