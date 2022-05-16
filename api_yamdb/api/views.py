from rest_framework import viewsets
from reviews.models import User, Comments, Titles, Reviews
from .serializers import UserSerializer, ReviewSerializer, CommentsSerializer, TitleSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUpViewSet(viewsets.ModelViewSet):
    pass

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer 
    pagination_class = PageNumberPagination
    # Теперь анонимным GET-запросом по-прежнему можно получить информацию  
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        new_queryset = Reviews.objects.filter(title=title)
        return new_queryset



        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination 
    # Теперь анонимным GET-запросом по-прежнему можно получить информацию 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer 

