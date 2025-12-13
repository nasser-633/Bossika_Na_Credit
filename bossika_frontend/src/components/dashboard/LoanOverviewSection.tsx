import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { DollarSign, Building2, Users, Landmark, HandCoins, BarChart3 } from 'lucide-react';

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

export default function LoanOverviewSection() {
  const [selectedProvider, setSelectedProvider] = useState<string>('');

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
    localStorage.setItem('loanOverview', JSON.stringify(data));
    alert(`Loan provider: ${data.providerType}\nAmount: KES ${Number(data.amount).toLocaleString()}`);
  };

  const handleProviderChange = (value: string) => {
    setSelectedProvider(value);
    setValue('providerType', value as any);
  };

  const handleStartChart = () => {
    if (selectedProvider) {
      const amountInput = document.getElementById('amount') as HTMLInputElement;
      if (amountInput && amountInput.value) {
        alert('Chart feature coming soon!');
      } else {
        alert('Please enter a loan amount first');
      }
    } else {
      alert('Please select a loan provider first');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-2">
          Loan Overview
        </h2>
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
                Choose a loan provider from the available options
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
                <Label htmlFor="amount">Amount (KES)</Label>
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
                  Enter the total loan amount in Kenyan Shillings
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row justify-end gap-3">
            <Button
              type="button"
              variant="outline"
              className="border-green-600 text-green-600 hover:bg-green-50"
              onClick={handleStartChart}
            >
              <BarChart3 className="mr-2 h-4 w-4" />
              Start Chart
            </Button>
            <Button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700"
            >
              Save Loan Details
            </Button>
          </div>
        </div>
      </form>
    </div>
  );
}
