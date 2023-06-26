from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.users.views import UserViewSet, UserFollowView


router = DefaultRouter()
router.register(
    '',
    UserViewSet,
    basename='user',
)


urlpatterns = [
    path('<int:pk>/follow', UserFollowView.as_view()),
    path('token/create/', cache_page(60*60*3)(TokenObtainPairView.as_view())),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

    # path('test/', TestView.as_view())
]
urlpatterns += router.urls
