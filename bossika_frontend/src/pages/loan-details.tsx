import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, CheckCircle } from 'lucide-react';
import { useEffect, useState } from 'react';

export default function LoanDetails() {
  const navigate = useNavigate();
  const [loanData, setLoanData] = useState<any>(null);

  useEffect(() => {
    // Retrieve loan overview data
    const savedData = localStorage.getItem('loanOverview');
    if (savedData) {
      setLoanData(JSON.parse(savedData));
    } else {
      // If no data, redirect back to overview
      navigate('/loan-overview');
    }
  }, [navigate]);

  const providerLabels: Record<string, string> = {
    bank: 'Bank',
    microfinance: 'Microfinance',
    cooperative: 'Cooperative',
    individual: 'Individual Lender',
  };

  if (!loanData) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <Button
            variant="ghost"
            onClick={() => navigate('/loan-overview')}
            className="mb-4"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Overview
          </Button>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            Loan Details
          </h1>
          <p className="text-gray-600">
            Add more details about your loan
          </p>
        </div>

        {/* Summary Card */}
        <Card className="mb-6 border-green-200 bg-green-50">
          <CardHeader>
            <div className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <CardTitle className="text-green-900">Overview Completed</CardTitle>
            </div>
            <CardDescription className="text-green-700">
              You selected: <strong>{providerLabels[loanData.providerType]}</strong> | 
              Loan Amount: <strong>{Number(loanData.amount).toLocaleString()} CFA</strong>
            </CardDescription>
          </CardHeader>
        </Card>

        {/* Placeholder for additional form sections */}
        <Card>
          <CardHeader>
            <CardTitle>Additional Details</CardTitle>
            <CardDescription>
              This page is under construction. More loan detail fields will be added here.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">
              Future fields may include:
            </p>
            <ul className="list-disc list-inside text-gray-600 mt-2 space-y-1">
              <li>Interest rate</li>
              <li>Loan duration</li>
              <li>Payment schedule</li>
              <li>Purpose of loan</li>
              <li>Collateral information</li>
            </ul>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <div className="flex justify-between items-center pt-6">
          <Button
            variant="outline"
            onClick={() => navigate('/loan-overview')}
          >
            Back
          </Button>
          <Button
            className="bg-blue-600 hover:bg-blue-700"
            onClick={() => navigate('/dashboard')}
          >
            Return to Dashboard
          </Button>
        </div>
      </div>
    </div>
  );
}
