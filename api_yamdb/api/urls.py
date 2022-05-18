from django.urls import path

from .views import APIToken, APIOneUser, APISignup, APIMe, APIUser


urlpatterns = [
    path('v1/auth/signup/', APISignup.as_view()),
    path('v1/auth/token/', APIToken.as_view()),
    path('v1/users/', APIUser.as_view()),
    path('v1/users/me/', APIMe.as_view()),
    path('v1/users/<str:username>/', APIOneUser.as_view()),
]