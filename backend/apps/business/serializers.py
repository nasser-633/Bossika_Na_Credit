from rest_framework import serializers
from apps.business.models import BusinessProfile
from apps.users.serializers import UserSerializer


class BusinessProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_net_cash_flow = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model = BusinessProfile
        fields = [
            'id',
            'user',
            'business_name',
            'business_type',
            'address',
            'size',
            'operation_period',
            'total_net_cash_flow',
        ]
