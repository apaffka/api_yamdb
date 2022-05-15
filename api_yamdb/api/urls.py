from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
from api.views import ReviewViewSet, CommentViewSet, TitleViewSet

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'titles', TitleViewSet, basename='titles')
# router_v1.register(r'categories', CategoriesViewSet, basename='categories')
# router_v1.register(r'genres', GenresViewSet, basename='genres')
# router_v1.register(r'reviews', ReviewViewSet, basename='reviews')
router_v1.register(r'comments', CommentViewSet, basename='comments')
router_v1.register(r'titles/(?P<title_id>[^/.]+)/reviews',
                   CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('auth/signup/', )
    # path('auth/token/', )
]