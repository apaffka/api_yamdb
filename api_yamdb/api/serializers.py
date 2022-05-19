from rest_framework import serializers
from reviews.models import Reviews, Comments, Titles
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from reviews.models import User
import numpy

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User

class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = Comments
        fields = ('id','author','pub_date','text') 


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
        
    )
    new_scores = serializers.SerializerMethodField('get_new_scores')


    class Meta:
        fields = ('id','author','text','score','pub_date','title','new_scores')
        model = Reviews

        
# На одно произведение пользователь может оставить только один отзыв.
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=('title', 'author')
                )
            ]

    def get_new_scores(self, obj):
        try:
            title_id = obj.title_id
            title_id = numpy.mean(title_id)
        except ValueError:
                # Иначе возвращаем ошибку
                raise serializers.ValidationError('Не возможно посчитать рейтинг')
            # Возвращаем данные в новом формате
        return title_id


       
class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = '__all__' 