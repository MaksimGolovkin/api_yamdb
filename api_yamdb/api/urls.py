from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (CategoryViewSet, GenreViewSet,
                       TitleViewSet, ReviewViewSet,
                       CommentViewSet, SignupViewSet,
                       TokenViewSet, UsersViewSet)

v1_router = SimpleRouter()
v1_router.register('auth/signup', SignupViewSet, basename='users')
v1_router.register('auth/token', TokenViewSet, basename='take_token')
v1_router.register('users', UsersViewSet, basename='users')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='reviews',)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments',)
urlpatterns = [
    path('v1/', include(v1_router.urls))
]
