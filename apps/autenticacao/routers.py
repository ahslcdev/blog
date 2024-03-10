from rest_framework.routers import DefaultRouter

from apps.autenticacao.viewsets import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)