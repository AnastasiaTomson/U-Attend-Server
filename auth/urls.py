from django.urls import path

from .views import AuthAPIView, refresh_token_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    path('refresh/', refresh_token_view, name='token_refresh'),
    path('login/', AuthAPIView.as_view()),
]
