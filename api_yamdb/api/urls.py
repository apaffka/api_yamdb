from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    APIToken, APISignup, CategoriesViewSet, GenresViewSet, TitlesViewSet,
    CommentViewSet, ReviewViewSet, UserViewSet
)

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genre')
router_v1.register(r'titles', TitlesViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignup.as_view()),
    path('v1/auth/token/', APIToken.as_view()),
]
