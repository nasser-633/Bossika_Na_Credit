from rest_framework import serializers
from apps.cashflow.models import CashFlow


class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = [
            'id', 'business', 'month', 'year', 'is_daily_cashflow',
            'cashflow_type', 'category', 'amount', 'balance',
            'date_recorded', 'created_at', 'updated_at'
        ]
        read_only_fields = ['balance', 'created_at', 'updated_at']
