from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')
# router_v1.register(r'titles', TitlesViewSet, basename='titles')
# router_v1.register(r'categories', CategoriesViewSet, basename='categories')
# router_v1.register(r'genres', GenresViewSet, basename='genres')
# router_v1.register(r'reviews', ReviewsViewSet, basename='reviews')
# router_v1.register(r'comments', CommentsViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('auth/signup/', )
    # path('auth/token/', )
]