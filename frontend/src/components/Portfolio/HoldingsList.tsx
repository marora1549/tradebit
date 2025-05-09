import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { format } from 'date-fns';
import { Search } from 'lucide-react';
import { api } from '../../services/api';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';

interface Holding {
  id: number;
  quantity: number;
  avg_price: number;
  purchase_date: string;
  total_value: number;
  stock_details: {
    id: number;
    symbol: string;
    name: string;
    sector: string;
    industry: string;
  };
}

const HoldingsList: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const { data, isLoading, error, refetch } = useQuery<{ results: Holding[] }>(
    'holdings',
    async () => {
      const response = await api.get('/portfolio/holdings/');
      return response.data;
    }
  );
  
  const filteredHoldings = data?.results.filter((holding) => {
    const searchLower = searchTerm.toLowerCase();
    return (
      holding.stock_details.symbol.toLowerCase().includes(searchLower) ||
      holding.stock_details.name.toLowerCase().includes(searchLower) ||
      holding.stock_details.sector?.toLowerCase().includes(searchLower) ||
      holding.stock_details.industry?.toLowerCase().includes(searchLower)
    );
  });
  
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Holdings</CardTitle>
        <div className="flex space-x-2">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
            <Input
              type="text"
              placeholder="Search holdings..."
              className="pl-8 w-full md:w-[200px] lg:w-[300px]"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <Button
            variant="outline"
            onClick={() => refetch()}
            isLoading={isLoading}
          >
            Refresh
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-700"></div>
          </div>
        ) : error ? (
          <div className="text-center py-10">
            <p className="text-gray-500">Failed to load holdings data.</p>
          </div>
        ) : filteredHoldings?.length === 0 ? (
          <div className="text-center py-10">
            <p className="text-gray-500">
              {searchTerm
                ? 'No holdings matching your search.'
                : 'No holdings found. Start by adding some stocks to your portfolio.'}
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4">Symbol</th>
                  <th className="text-left py-3 px-4">Name</th>
                  <th className="text-right py-3 px-4">Quantity</th>
                  <th className="text-right py-3 px-4">Avg. Price</th>
                  <th className="text-right py-3 px-4">Value</th>
                  <th className="text-left py-3 px-4">Purchase Date</th>
                  <th className="text-left py-3 px-4">Sector</th>
                </tr>
              </thead>
              <tbody>
                {filteredHoldings?.map((holding) => (
                  <tr key={holding.id} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-4 font-medium">{holding.stock_details.symbol}</td>
                    <td className="py-3 px-4">{holding.stock_details.name}</td>
                    <td className="py-3 px-4 text-right">{holding.quantity}</td>
                    <td className="py-3 px-4 text-right">
                      ₹{holding.avg_price.toLocaleString('en-IN', {
                        maximumFractionDigits: 2,
                        minimumFractionDigits: 2,
                      })}
                    </td>
                    <td className="py-3 px-4 text-right font-medium">
                      ₹{holding.total_value.toLocaleString('en-IN', {
                        maximumFractionDigits: 2,
                        minimumFractionDigits: 2,
                      })}
                    </td>
                    <td className="py-3 px-4">
                      {format(new Date(holding.purchase_date), 'dd MMM yyyy')}
                    </td>
                    <td className="py-3 px-4">{holding.stock_details.sector || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default HoldingsList;
