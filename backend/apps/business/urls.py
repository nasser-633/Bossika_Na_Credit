from django.urls import path, include
from rest_framework import routers
from .views import BusinessProfileViewSet, BusinessHealthAPIView

router = routers.DefaultRouter()
router.register(r'business', BusinessProfileViewSet, basename='business')

urlpatterns = [
    path('', include(router.urls)),
    path('business/<int:pk>/health/', BusinessHealthAPIView.as_view(), name='business-health'),
]
