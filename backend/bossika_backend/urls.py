"""
URL configuration for bossika_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from apps.cashflow.views import CashFlowViewSet
from apps.loans.views import BusinessLoansViewSet, LoanRepaymentViewSet
from apps.business.views import BusinessProfileViewSet, BusinessHealthAPIView
from apps.users.views import RegisterAPIView, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger/OpenAPI
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Bossika API",
        default_version='v1',
        description="API docs for Bossika",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'business', BusinessProfileViewSet, basename='business')
router.register(r'cashflows', CashFlowViewSet, basename='cashflow')
router.register(r'loans', BusinessLoansViewSet, basename='loans')
router.register(r'loan-repayments', LoanRepaymentViewSet, basename='loan-repayments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterAPIView.as_view(), name='register'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/business/<int:pk>/health/', BusinessHealthAPIView.as_view(), name='business-health'),

    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
