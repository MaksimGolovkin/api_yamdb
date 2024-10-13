from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet,
                       UsersViewSet, signup, token)


app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('users', UsersViewSet, basename='users')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments')
urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup, name='users_signup'),
    path('v1/auth/token/', token, name='take_token_users'),
]
