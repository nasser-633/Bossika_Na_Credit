from django.urls import path, include
from rest_framework import routers
from .views import CashFlowViewSet

router = routers.DefaultRouter()
router.register(r'cashflows', CashFlowViewSet, basename='cashflow')

urlpatterns = [
    path('', include(router.urls)),
]
