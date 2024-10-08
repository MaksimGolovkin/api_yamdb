from django.urls import include, path

from api.views import SignupViewSet, TokenViewSet, UsersViewSet
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register('auth/signup', SignupViewSet, basename='users_signup')
v1_router.register('auth/token', TokenViewSet, basename='take_token_users')
v1_router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
