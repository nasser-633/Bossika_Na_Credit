from rest_framework.test import APITestCase
from rest_framework import status


class APIIntegrationTests(APITestCase):
    def setUp(self):
        self.register_url = '/api/auth/register/'
        self.token_url = '/api/auth/token/'
        self.business_url = '/api/business/'
        self.cashflow_url = '/api/cashflows/'
        self.loans_url = '/api/loans/'
        self.repayments_url = '/api/loan-repayments/'

    def test_full_flow(self):
        # Register
        reg_data = {
            "username": "alice",
            "password": "Pass1234",
            "email": "a@example.com",
        }
        r = self.client.post(self.register_url, reg_data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        access = r.data['access']

        # Create business
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        biz_data = {
            "business_name": "My Shop",
            "business_type": "RETAIL",
            "operation_period": 1.5,
        }
        r = self.client.post(self.business_url, biz_data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        business_id = r.data['id']

        # Create a cashflow (income)
        cf_data = {
            "business": business_id,
            "cashflow_type": "INCOME",
            "amount": "1000.00",
            "date_recorded": "2025-12-01",
        }
        r = self.client.post(self.cashflow_url, cf_data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertIn('balance', r.data)

        # Create loan
        loan_data = {
            "business": business_id,
            "lender": "Bank",
            "principal_amount": "5000.00",
            "interest_rate": 0.1,
            "loan_period": 1,
        }
        r = self.client.post(self.loans_url, loan_data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        loan_id = r.data['id']

        # Create repayment (valid)
        repay_data = {
            "business_loan": loan_id,
            "amount_paid": "1000.00",
            "date_paid": "2025-12-15",
        }
        r = self.client.post(self.repayments_url, repay_data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        # Overpay should be rejected
        overpay_data = {
            "business_loan": loan_id,
            "amount_paid": "9999999.00",
            "date_paid": "2025-12-16",
        }
        r = self.client.post(self.repayments_url, overpay_data, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        # Business health
        r = self.client.get(f"/api/business/{business_id}/health/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn('net_cash_flow', r.data)

