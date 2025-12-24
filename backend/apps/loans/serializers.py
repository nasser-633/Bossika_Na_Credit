from rest_framework import serializers
from apps.loans.models import BusinessLoans, LoanRepayment
from decimal import Decimal


class LoanRepaymentSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # Ensure repayment does not exceed remaining loan balance.
        loan = data.get('business_loan')
        if loan is None and self.instance:
            loan = getattr(self.instance, 'business_loan', None)

        amount = data.get('amount_paid')
        if amount is None and self.instance:
            amount = getattr(self.instance, 'amount_paid', None)

        if loan is None or amount is None:
            return data

        # loan.balance is a Decimal or numeric; convert amount to Decimal for safe comparison
        remaining = loan.balance
        # If updating an existing repayment, add back the original amount to remaining
        if self.instance is not None:
            remaining += Decimal(self.instance.amount_paid)

        if Decimal(amount) > Decimal(remaining):
            raise serializers.ValidationError({
                'amount_paid': 'Repayment exceeds the remaining loan balance.'
            })

        return data

    class Meta:
        model = LoanRepayment
        fields = [
            'id',
            'business_loan',
            'amount_paid',
            'date_paid',
            'payment_is_late',
            'late_fee_charged',
            'created_at',
            'updated_at',
        ]


class BusinessLoansSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    total_amount = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    interest_amount = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    repayments = LoanRepaymentSerializer(many=True, read_only=True)

    class Meta:
        model = BusinessLoans
        fields = [
            'id',
            'business',
            'reason',
            'lender',
            'category',
            'installments_per_month',
            'principal_amount',
            'interest_rate',
            'loan_period',
            'date_of_loan',
            'loan_status',
            'interest_amount',
            'total_amount',
            'balance',
            'repayments',
            'created_at',
            'updated_at',
        ]
