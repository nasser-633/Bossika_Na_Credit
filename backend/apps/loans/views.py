from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.loans.models import BusinessLoans, LoanRepayment
from apps.loans.serializers import BusinessLoansSerializer, LoanRepaymentSerializer
from apps.core.permissions import IsOwnerOrAdmin


class BusinessLoansViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessLoansSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return BusinessLoans.objects.all().order_by('-date_of_loan')
        return BusinessLoans.objects.filter(business__user=user).order_by('-date_of_loan')

    def perform_create(self, serializer):
        business = serializer.validated_data.get('business')
        if not (self.request.user.is_staff or business.user == self.request.user):
            raise PermissionError('Cannot create loan for this business')
        serializer.save()


class LoanRepaymentViewSet(viewsets.ModelViewSet):
    serializer_class = LoanRepaymentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return LoanRepayment.objects.all().order_by('-date_paid')
        return LoanRepayment.objects.filter(business_loan__business__user=user).order_by('-date_paid')

    def perform_create(self, serializer):
        # validate loan ownership
        loan = serializer.validated_data.get('business_loan')
        if not (self.request.user.is_staff or loan.business.user == self.request.user):
            raise PermissionError('Cannot create repayment for this loan')
        serializer.save()


