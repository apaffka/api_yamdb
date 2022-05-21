from rest_framework import serializers

from reviews.models import User, Categories, Genres, Titles


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
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = '__all__'
