import React, { useState } from 'react';
import { Outlet, NavLink, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { LayoutDashboard, FileText, Settings, LogOut, Menu, X, LineChart } from 'lucide-react';
import { Button } from '../components/ui/Button';

const DashboardLayout: React.FC = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  const handleLogout = () => {
    logout();
    navigate('/auth/login');
  };
  
  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Portfolio', href: '/portfolio', icon: FileText },
    { name: 'Zerodha Integration', href: '/zerodha', icon: LineChart },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];
  
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };
  
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 md:hidden"
          onClick={toggleSidebar}
        ></div>
      )}
      
      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 md:translate-x-0 md:static md:h-screen md:z-auto`}
      >
        <div className="flex items-center justify-between h-16 px-4 border-b">
          <Link to="/" className="text-xl font-bold text-primary-700">
            TradeBit
          </Link>
          <button
            className="p-1 rounded-md md:hidden focus:outline-none focus:ring-2 focus:ring-primary-500"
            onClick={toggleSidebar}
          >
            <X className="h-6 w-6" />
          </button>
        </div>
        
        <nav className="px-2 py-4 h-full flex flex-col">
          <div className="space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <NavLink
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon
                    className={`mr-3 h-5 w-5 ${
                      isActive ? 'text-primary-700' : 'text-gray-500'
                    }`}
                  />
                  {item.name}
                </NavLink>
              );
            })}
          </div>
          
          <div className="mt-auto border-t pt-4">
            <div className="px-3 py-2">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 rounded-full bg-primary-700 flex items-center justify-center text-white font-medium">
                    {user?.username?.charAt(0).toUpperCase() || 'U'}
                  </div>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-700">
                    {user?.username || 'User'}
                  </p>
                  <p className="text-xs text-gray-500">
                    {user?.email || 'user@example.com'}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="px-3 py-2">
              <Button
                variant="ghost"
                className="w-full justify-start text-gray-700 hover:bg-gray-100"
                onClick={handleLogout}
              >
                <LogOut className="mr-3 h-5 w-5 text-gray-500" />
                Log out
              </Button>
            </div>
          </div>
        </nav>
      </div>
      
      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top header */}
        <header className="bg-white shadow-sm z-10">
          <div className="px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <button
              className="p-1 rounded-md md:hidden focus:outline-none focus:ring-2 focus:ring-primary-500"
              onClick={toggleSidebar}
            >
              <Menu className="h-6 w-6" />
            </button>
            <div className="text-lg font-medium md:hidden">
              TradeBit
            </div>
            <div>  
              {/* Placeholder for future header elements */}
            </div>
          </div>
        </header>
        
        {/* Main content area */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
