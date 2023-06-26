from rest_framework.routers import DefaultRouter

from apps.posts.views import PostViewSet


router = DefaultRouter()
router.register(
    '',
    PostViewSet,
    basename='post'
)

urlpatterns = router.urls
