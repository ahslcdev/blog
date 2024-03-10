from django.urls import path
from .views import login_page, logout_page
from apps.autenticacao.views import CustomAccessToken, CustomRefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('login/', login_page, name="login"),
    path('token/', CustomAccessToken.as_view(), name="access_token"),
    path('token/refresh/', CustomRefreshToken.as_view(), name="refresh_token"),
    path('blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('logout/', logout_page, name='logout')
]