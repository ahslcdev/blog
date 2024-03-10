from rest_framework.routers import DefaultRouter

from apps.core.viewsets import CommentsViewSet, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentsViewSet)