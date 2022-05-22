from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import User, Categories, Genre, Title, Review, Comments
from .permissions import (IsAdministrator, IsModerator, IsSuperuser, IsUser, CommentRewiewPermission)
from .serializers import (SignupSerializer,
                          TokenSerializer, MeSerializer, OneUserSerializer,
                          MeAdminSerializer, UserSerializer,
                          CategoriesSerializer, GenreSerializer,
                          TitlesSerializer, ReviewSerializer,CommentSerializer  )
from .token import default_token_generator, get_tokens_for_user
from .mailing import send_email
from django.db.models import Avg


class APIUser(APIView, LimitOffsetPagination):
    permission_classes = [IsAdministrator | IsSuperuser]

    def get(self, request):
        user = User.objects.all()
        results = self.paginate_queryset(user, request, view=self)
        serializer = UserSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIOneUser(APIView):
    permission_classes = [IsAdministrator | IsSuperuser]

    def get_object(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, username):
        user = self.get_object(username)
        serializer = OneUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = self.get_object(username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APISignup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            email = serializer.data['email']
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
            )
            if created is True:
                token = default_token_generator.make_token(user)
                User.objects.filter(username=username).update(
                    code=token, is_active=True
                )
                send_email(token, email)
                return Response({'email': email, 'username': username})
            else:
                token = default_token_generator.make_token(user)
                User.objects.filter(username=username).update(code=token)
                send_email(token, email)
                return Response({'email': email, 'username': username})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIToken(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=self.request.data['username']
            )
            token = self.request.data['confirmation_code']
            check_token = default_token_generator.check_token(user, token)
            if check_token is True:
                User.objects.filter(
                    username=self.request.data['username']
                ).update(is_active=True)
            if check_token is False:
                return Response(
                    {'message': 'Код не прошёл проверку!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'token': f'{get_tokens_for_user(user)}'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIMe(APIView):
    permission_classes = [IsUser | IsAdministrator | IsModerator]

    def get(self, request):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        serializer = MeAdminSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        username = request.user.get_username()
        user = get_object_or_404(User, username=username)
        if user.role == 'user':
            serializer = MeSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = MeAdminSerializer(
                user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return super().get_permissions()
        return (IsAdministrator(),)


class GenresViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return super().get_permissions()
        return (IsAdministrator(),)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitlesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year',)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return super().get_permissions()
        return (IsAdministrator(),)

    def get_queryset(self):
        queryset = self.queryset
        genre_slug = self.request.query_params.get('genre')
        category_slug = self.request.query_params.get('category')
        name = self.request.query_params.get('name')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CommentRewiewPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CommentRewiewPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
