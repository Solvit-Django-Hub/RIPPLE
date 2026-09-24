
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    ProfileAPIView,
    VerifyEmailAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('profile/', ProfileAPIView.as_view(), name='api_profile'),

   
    path('verify-email/', VerifyEmailAPIView.as_view(), name='api_verify_email'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='api_password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmAPIView.as_view(), name='api_password_reset_confirm'),
]