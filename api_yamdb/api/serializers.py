from rest_framework import serializers
from reviews.models import Reviews, Comments, Titles

from reviews.models import User


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
    class Meta:
        model = Comments
        fields = '__all__' 


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        # comments = CommentsSerializer(many=True)  
        fields = ('id','text', 'author', 'score', 'pub_date','title','comments') 
       
class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = '__all__' 