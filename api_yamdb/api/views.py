from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        SAFE_METHODS, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import User, Categories, Genre, Title
from .filters import TitleFilter
from .permissions import (IsAdministrator, CommentRewiewPermission,
                          GenresTitlesPermission)
from .serializers import (SignupSerializer, TokenSerializer, UserSerializer,
                          CategoriesSerializer, GenreSerializer,
                          TitlesSerializer, ReviewSerializer,
                          CommentSerializer)
from .token import default_token_generator, get_tokens_for_user
from .mailing import send_email
from django.db.models import Avg


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdministrator]
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class MyOwnViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class CategoriesViewSet(MyOwnViewSet):
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


class GenresViewSet(MyOwnViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [GenresTitlesPermission]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitlesSerializer
    permission_classes = [GenresTitlesPermission]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    # filterset_fields = ('year',)
    #
    # def get_queryset(self):
    #     queryset = self.queryset
    #     genre_slug = self.request.query_params.get('genre')
    #     category_slug = self.request.query_params.get('category')
    #     name = self.request.query_params.get('name')
    #     if genre_slug:
    #         queryset = queryset.filter(genre__slug=genre_slug)
    #     if category_slug:
    #         queryset = queryset.filter(category__slug=category_slug)
    #     if name:
    #         queryset = queryset.filter(name__icontains=name)
    #     return queryset


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
