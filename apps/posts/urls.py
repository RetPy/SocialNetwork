from rest_framework.routers import DefaultRouter
from django.urls import path

from apps.posts.views import PostViewSet, LikeAPIView


router = DefaultRouter()
router.register(
    '',
    PostViewSet,
    basename='post'
)
urlpatterns = [
    path('<int:pk>/likes/', LikeAPIView.as_view())
]
urlpatterns += router.urls
