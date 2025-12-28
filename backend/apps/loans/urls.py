from django.urls import path, include
from rest_framework import routers
from .views import BusinessLoansViewSet, LoanRepaymentViewSet

router = routers.DefaultRouter()
router.register(r'loans', BusinessLoansViewSet, basename='loans')
router.register(r'loan-repayments', LoanRepaymentViewSet, basename='loan-repayments')

urlpatterns = [
    path('', include(router.urls)),
]
