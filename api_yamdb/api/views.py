from rest_framework import viewsets
from reviews.models import User, Comments, Titles, Reviews
from .serializers import UserSerializer, ReviewSerializer, CommentsSerializer, TitleSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response


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

    def create(self, request, *args, **kwargs):
            serializer = ReviewSerializer(data=request.data)
            title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
            if serializer.is_valid():
                serializer.save(author=request.user, title=title)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination 
    # Теперь анонимным GET-запросом по-прежнему можно получить информацию 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

    
    def get_queryset(self):
       title_id = self.kwargs.get('title_id')
       title = get_object_or_404(Titles, id=title_id)
       review = get_object_or_404(title.reviews, id = self.kwargs.get('review_id'))
       return  review.comments.all()

    def create(self, request, *args, **kwargs):
            serializer = CommentsSerializer(data=request.data)
            title_id = self.kwargs.get('title_id')
            title = get_object_or_404(Titles, id=title_id)
            review = get_object_or_404(title.reviews, id = self.kwargs.get('review_id'))
            if serializer.is_valid():
                serializer.save(author=self.request.user, review=review)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer 

