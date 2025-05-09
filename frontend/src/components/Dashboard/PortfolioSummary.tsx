import React from 'react';
import { useQuery } from 'react-query';
import { format } from 'date-fns';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { api } from '../../services/api';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';

interface PortfolioSummaryData {
  total_value: number;
  total_holdings: number;
  sectors: Record<string, number>;
  top_holdings: Array<{
    id: number;
    stock_details: {
      symbol: string;
      name: string;
    };
    quantity: number;
    avg_price: number;
    total_value: number;
  }>;
}

const PortfolioSummary: React.FC = () => {
  const { data, isLoading, error } = useQuery<PortfolioSummaryData>(
    'portfolioSummary',
    async () => {
      const response = await api.get('/portfolio/summary/');
      return response.data;
    }
  );

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Portfolio Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-700"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error || !data) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Portfolio Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-10">
            <p className="text-gray-500">Failed to load portfolio data.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Format sector data for the chart
  const sectorData = Object.entries(data.sectors).map(([name, value]) => ({
    name,
    value: parseFloat(value.toFixed(2)),
  }));

  // Calculate colors for sectors
  const COLORS = [
    '#4f46e5', // primary-700
    '#6366f1',
    '#8b5cf6',
    '#a855f7',
    '#d946ef',
    '#ec4899',
    '#f43f5e',
  ];

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Portfolio Summary</CardTitle>
        <p className="text-sm text-gray-500">
          As of {format(new Date(), 'dd MMM yyyy')}
        </p>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div className="space-y-4">
              <div>
                <h4 className="text-sm font-medium text-gray-500">Total Value</h4>
                <p className="text-2xl font-bold">
                  ₹{data.total_value.toLocaleString('en-IN', {
                    maximumFractionDigits: 2,
                    minimumFractionDigits: 2,
                  })}
                </p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-500">Holdings</h4>
                <p className="text-2xl font-bold">{data.total_holdings}</p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-500 mb-2">Top Holdings</h4>
                <div className="space-y-2">
                  {data.top_holdings.map((holding) => (
                    <div key={holding.id} className="flex justify-between">
                      <div>
                        <p className="font-medium">{holding.stock_details.symbol}</p>
                        <p className="text-xs text-gray-500">{holding.stock_details.name}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-medium">
                          ₹{holding.total_value.toLocaleString('en-IN', {
                            maximumFractionDigits: 2,
                            minimumFractionDigits: 2,
                          })}
                        </p>
                        <p className="text-xs text-gray-500">
                          {holding.quantity} × ₹{holding.avg_price}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
          
          <div>
            <h4 className="text-sm font-medium text-gray-500 mb-2">Sector Allocation</h4>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sectorData} layout="vertical">
                  <XAxis type="number" />
                  <YAxis 
                    dataKey="name" 
                    type="category" 
                    width={100}
                    tick={{ fontSize: 12 }}
                  />
                  <Tooltip 
                    formatter={(value) => [`₹${value}`, 'Value']}
                    labelFormatter={(label) => `Sector: ${label}`}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                    {sectorData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PortfolioSummary;
