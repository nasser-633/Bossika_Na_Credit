from rest_framework import viewsets, permissions
from apps.business.models import BusinessProfile
from apps.business.serializers import BusinessProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BusinessProfileViewSet(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # During schema generation `request` may be None or the
        # user may be an AnonymousUser (swagger_fake_view). Short-
        # circuit in that case.
        if getattr(self, 'swagger_fake_view', False):
            return BusinessProfile.objects.none()
        request = getattr(self, 'request', None)
        if request is None:
            return BusinessProfile.objects.none()
        user = request.user
        if user.is_anonymous:
            return BusinessProfile.objects.none()
        # limit to businesses owned by requesting user
        return BusinessProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BusinessHealthAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        # Expect pk as business id in URL
        try:
            business = BusinessProfile.objects.get(pk=pk)
        except BusinessProfile.DoesNotExist:
            return Response({'detail': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

        net_cash_flow = business.total_net_cash_flow
        total_loan_balance = sum(
            loan.balance for loan in business.business_loans.all()
        )

        loan_coverage = None
        try:
            if total_loan_balance:
                loan_coverage = float(net_cash_flow) / float(total_loan_balance)
        except Exception:
            loan_coverage = None

        data = {
            'business_id': business.id,
            'business_name': business.business_name,
            'net_cash_flow': net_cash_flow,
            'total_loan_balance': total_loan_balance,
            'loan_coverage_ratio': loan_coverage,
        }
        # Simple advice rules
        advice = []
        # low net cash flow relative to loans -> reduce debt
        try:
            if loan_coverage is not None and loan_coverage < 0.2:
                advice.append('Reduce debt: loan burden is high relative to cash flow')
        except Exception:
            pass

        # If business is very young and has outstanding loans, advise caution/expansion only if profitable
        if business.operation_period and float(business.operation_period) < 1:
            advice.append('Business is young; avoid aggressive expansion')

        if total_loan_balance == 0:
            advice.append('No outstanding loans; consider expansion if net cash flow is positive')

        data['advice'] = advice
        return Response(data)
