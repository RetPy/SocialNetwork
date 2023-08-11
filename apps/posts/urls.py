from rest_framework.routers import DefaultRouter
from django.urls import path

from apps.posts.views import PostViewSet, LikeAPIView, CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView


router = DefaultRouter()
router.register(
    '',
    PostViewSet,
    basename='post'
)
urlpatterns = [
    path('<int:pk>/likes/', LikeAPIView.as_view()),
    path('<int:pk>/comments/', CommentListCreateAPIView.as_view()),
    path('<int:pk>/comments/<int:comm_pk>', CommentRetrieveUpdateDestroyAPIView.as_view())
]
urlpatterns += router.urls
