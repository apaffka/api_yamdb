from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    APIToken, APIOneUser, APISignup, APIMe, APIUser,
    CategoriesViewSet, GenresViewSet, TitlesViewSet, ReviewViewSet, 
    CommentViewSet
)

router_v1 = DefaultRouter()

router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'titles', TitlesViewSet, basename='titles')
router_v1.register('reviews', ReviewViewSet, basename='reviews')
router_v1.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignup.as_view()),
    path('v1/auth/token/', APIToken.as_view()),
    path('v1/users/', APIUser.as_view()),
    path('v1/users/me/', APIMe.as_view()),
    path('v1/users/<str:username>/', APIOneUser.as_view()),
]
