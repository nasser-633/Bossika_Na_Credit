import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, DollarSign, Building2, Users, Landmark, HandCoins, FileText, LayoutDashboard, BarChart3 } from 'lucide-react';

const loanSchema = z.object({
  providerType: z.enum(['tala', 'branch', 'zenka', 'fuliza', 'kcb-mpesa', 'mshwari', 'okoa-stima', 'timiza', 'eazzy-loan', 'equity-eazzy'], {
    message: 'Please select a loan provider',
  }),
  amount: z.string()
    .min(1, 'Loan amount is required')
    .refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
      message: 'Amount must be a positive number',
    }),
});

type LoanFormData = z.infer<typeof loanSchema>;

const loanProviders = [
  {
    id: 'tala',
    label: 'Tala',
    description: 'Quick mobile loans up to KES 50,000',
    icon: DollarSign,
  },
  {
    id: 'branch',
    label: 'Branch',
    description: 'Instant loans via mobile app',
    icon: Building2,
  },
  {
    id: 'zenka',
    label: 'Zenka',
    description: 'Fast approval digital loans',
    icon: HandCoins,
  },
  {
    id: 'fuliza',
    label: 'Fuliza M-PESA',
    description: 'M-PESA overdraft service',
    icon: DollarSign,
  },
  {
    id: 'kcb-mpesa',
    label: 'KCB M-PESA',
    description: 'Bank and M-PESA loan facility',
    icon: Landmark,
  },
  {
    id: 'mshwari',
    label: 'M-Shwari',
    description: 'Safaricom & NCBA Bank service',
    icon: Building2,
  },
  {
    id: 'okoa-stima',
    label: 'Okoa Stima',
    description: 'KPLC prepaid token loan',
    icon: HandCoins,
  },
  {
    id: 'timiza',
    label: 'Timiza',
    description: 'Barclays Bank mobile loans',
    icon: Landmark,
  },
  {
    id: 'eazzy-loan',
    label: 'Eazzy Loan',
    description: 'Equity Bank instant loans',
    icon: Building2,
  },
  {
    id: 'equity-eazzy',
    label: 'Equity Eazzy',
    description: 'Equity Bank mobile banking loans',
    icon: Users,
  },
];

export default function LoanOverview() {
  const navigate = useNavigate();
  const [selectedProvider, setSelectedProvider] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'overview' | 'articles'>('overview');

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<LoanFormData>({
    resolver: zodResolver(loanSchema),
  });

  const onSubmit = (data: LoanFormData) => {
    console.log('Loan Overview Data:', data);
    // Store in localStorage or state management
    localStorage.setItem('loanOverview', JSON.stringify(data));
    // Navigate to next step (loan details page)
    navigate('/loan-details');
  };

  const handleProviderChange = (value: string) => {
    setSelectedProvider(value);
    setValue('providerType', value as any);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="flex h-screen">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r shadow-lg flex flex-col">
          <div className="p-6 border-b">
            <h2 className="text-xl font-bold text-gray-900">Loan Manager</h2>
            <p className="text-sm text-gray-600 mt-1">Manage your loans</p>
          </div>
          
          <nav className="flex-1 p-4">
            <button
              onClick={() => setActiveTab('overview')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-all mb-2 ${
                activeTab === 'overview'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <LayoutDashboard className="h-5 w-5" />
              <span className="font-medium">Overview</span>
            </button>
            
            <button
              onClick={() => setActiveTab('articles')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-all ${
                activeTab === 'articles'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <FileText className="h-5 w-5" />
              <span className="font-medium">Articles</span>
            </button>
          </nav>

          <div className="p-4 border-t">
            <Button
              variant="outline"
              onClick={() => navigate('/dashboard')}
              className="w-full"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Button>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto">
          <div className="p-4 md:p-8">
            {activeTab === 'overview' && (
              <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="mb-6">
                  <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                    Loan Overview
                  </h1>
                  <p className="text-gray-600">
                    Select your loan provider and enter the amount you need
                  </p>
                </div>

                <form onSubmit={handleSubmit(onSubmit)}>
                  <div className="space-y-6">
            {/* Loan Provider Selection */}
            <Card>
              <CardHeader>
                <CardTitle>Select Loan Provider</CardTitle>
                <CardDescription>
                  Choose the type of institution or individual providing the loan
                </CardDescription>
              </CardHeader>
              <CardContent>
                <RadioGroup
                  value={selectedProvider}
                  onValueChange={handleProviderChange}
                  className="grid grid-cols-1 md:grid-cols-2 gap-4"
                >
                  {loanProviders.map((provider) => {
                    const Icon = provider.icon;
                    return (
                      <div key={provider.id}>
                        <Label
                          htmlFor={provider.id}
                          className={`flex items-start space-x-3 p-4 rounded-lg border-2 cursor-pointer transition-all hover:bg-blue-50 ${
                            selectedProvider === provider.id
                              ? 'border-blue-600 bg-blue-50'
                              : 'border-gray-200'
                          }`}
                        >
                          <RadioGroupItem
                            value={provider.id}
                            id={provider.id}
                            className="mt-1"
                          />
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <Icon className="h-5 w-5 text-blue-600" />
                              <span className="font-semibold text-gray-900">
                                {provider.label}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600">
                              {provider.description}
                            </p>
                          </div>
                        </Label>
                      </div>
                    );
                  })}
                </RadioGroup>
                {errors.providerType && (
                  <p className="text-sm text-red-600 mt-2">
                    {errors.providerType.message}
                  </p>
                )}
              </CardContent>
            </Card>

            {/* Loan Amount Input */}
            <Card>
              <CardHeader>
                <CardTitle>Loan Amount</CardTitle>
                <CardDescription>
                  Enter the amount of loan you need or have taken
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Label htmlFor="amount">Amount (CFA)</Label>
                  <div className="relative">
                    <DollarSign className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                    <Input
                      id="amount"
                      type="number"
                      placeholder="Enter loan amount"
                      className="pl-10 text-lg"
                      {...register('amount')}
                    />
                  </div>
                  {errors.amount && (
                    <p className="text-sm text-red-600">
                      {errors.amount.message}
                    </p>
                  )}
                  <p className="text-xs text-gray-500 mt-1">
                    Enter the total loan amount in CFA francs
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Action Buttons */}
            <div className="flex justify-between items-center pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate(-1)}
              >
                Cancel
              </Button>
              <div className="flex gap-3">
                <Button
                  type="button"
                  variant="outline"
                  className="border-green-600 text-green-600 hover:bg-green-50"
                  onClick={() => {
                    if (selectedProvider && document.getElementById('amount') as HTMLInputElement) {
                      const amount = (document.getElementById('amount') as HTMLInputElement).value;
                      if (amount) {
                        // Navigate to chart/analytics page (to be created)
                        alert('Chart feature coming soon!');
                      }
                    }
                  }}
                >
                  <BarChart3 className="mr-2 h-4 w-4" />
                  Start Chart
                </Button>
                <Button
                  type="submit"
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  Continue
                </Button>
              </div>
            </div>
          </div>
        </form>
      </div>
            )}

            {activeTab === 'articles' && (
              <div className="max-w-4xl mx-auto">
                <div className="mb-6">
                  <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                    Loan Articles
                  </h1>
                  <p className="text-gray-600">
                    Browse helpful articles about loans and financial management
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                    <CardHeader>
                      <CardTitle className="text-lg">Understanding Loan Terms</CardTitle>
                      <CardDescription>
                        Learn about interest rates, repayment periods, and loan conditions
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-gray-600 mb-4">
                        A comprehensive guide to understanding loan terminology and making informed decisions...
                      </p>
                      <Button variant="link" className="p-0 h-auto text-blue-600">
                        Read More →
                      </Button>
                    </CardContent>
                  </Card>

                  <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                    <CardHeader>
                      <CardTitle className="text-lg">Choosing the Right Lender</CardTitle>
                      <CardDescription>
                        Compare different types of lenders and find the best fit
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-gray-600 mb-4">
                        Discover the pros and cons of banks, microfinance, and other lending options...
                      </p>
                      <Button variant="link" className="p-0 h-auto text-blue-600">
                        Read More →
                      </Button>
                    </CardContent>
                  </Card>

                  <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                    <CardHeader>
                      <CardTitle className="text-lg">Managing Loan Repayments</CardTitle>
                      <CardDescription>
                        Tips for staying on track with your loan payments
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-gray-600 mb-4">
                        Learn strategies to manage your cash flow and never miss a payment...
                      </p>
                      <Button variant="link" className="p-0 h-auto text-blue-600">
                        Read More →
                      </Button>
                    </CardContent>
                  </Card>

                  <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                    <CardHeader>
                      <CardTitle className="text-lg">Business Loan Best Practices</CardTitle>
                      <CardDescription>
                        How to use business loans effectively for growth
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-gray-600 mb-4">
                        Maximize the value of your business loan with these proven strategies...
                      </p>
                      <Button variant="link" className="p-0 h-auto text-blue-600">
                        Read More →
                      </Button>
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
