from django.urls import path, include
from rest_framework.routers import DefaultRouter
from portal_api.api_views.auth import LocalAuth
from portal_api.api_views.news import NewsViewSet
from portal_api.api_views.user import UserViewSet
from portal_api.api_views.user_profile import UserProfileViewSet
from portal_api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'users', UserViewSet)
router.register(r'profile', UserProfileViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('auth/', LocalAuth.as_view(), name='local_auth'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]


