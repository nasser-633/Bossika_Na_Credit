from django.urls import path, include
from rest_framework import routers
from .views import RegisterAPIView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
]
