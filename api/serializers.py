from accounts.models import User
from news.models import News
from posts.models import Post

from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')
        

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('__all__')

        
class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('__all__')
