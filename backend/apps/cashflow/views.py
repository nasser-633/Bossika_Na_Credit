from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.cashflow.models import CashFlow
from apps.cashflow.serializers import CashFlowSerializer
from apps.core.permissions import IsOwnerOrAdmin


class CashFlowViewSet(viewsets.ModelViewSet):
    serializer_class = CashFlowSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return CashFlow.objects.all().order_by('-date_recorded')
        # limit to cashflows whose business is owned by the requesting user
        return CashFlow.objects.filter(business__user=user).order_by('-date_recorded')

    def perform_create(self, serializer):
        # ensure the business provided belongs to the user (unless admin)
        business = serializer.validated_data.get('business')
        if not (self.request.user.is_staff or business.user == self.request.user):
            raise PermissionError('Cannot create cashflow for this business')
        serializer.save()

