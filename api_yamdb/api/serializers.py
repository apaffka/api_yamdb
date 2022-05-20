from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import User, Categories, Genres, Titles, Reviews, Comments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {
                    'username':
                        'Нельзя использовать имя me в качестве имени пользователя.'
                }
            )
        return data


class OneUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    username = serializers.CharField(allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {
                    'username':
                        'Нельзя использовать имя me в качестве имени пользователя.'
                },
            )
        elif User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                {
                    'username':
                        'Пользователь с данным username уже зарегистрирован.'
                },
            )
        elif User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {
                    'email':
                        'Пользователь с данным email уже зарегистрирвоан.'
                },
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(source='code')
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class MeSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MeAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug', many=True)
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug')
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Titles
        fields = (
            'id', 'name', 'year', 'category', 'genres', 'rating', 'description')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        genres = Genres.objects.filter(slug__in=data['genres'])
        category = Categories.objects.get(slug=data['category'])
        data['genres'] = GenresSerializer(instance=genres, many=True).data
        data['category'] = CategoriesSerializer(instance=category).data
        return data

class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        validators=[UniqueValidator(queryset=Comments.objects.all())]
    )
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    

    class Meta:
        model = Comments
        fields = ('id','author','pub_date','text','review') 


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
        
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='id')

    class Meta:
        fields = ('title', 'id', 'text', 'author', 'score', 'pub_date')
        model = Reviews

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Reviews.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError(
                'Повторно комментировать нельзя')
        return data

