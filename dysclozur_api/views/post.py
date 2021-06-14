from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from dysclozur_api.models import Post, DysclozurUser
from django.contrib.auth.models import User
from rest_framework.decorators import action

class PostView(ViewSet):
    """DYSCLOZUR POSTS"""
    
    def list(self, request):
        """Handle GET requests to POST resource
        Returns:
            Response -- JSON serialized list of posts
        """
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized post instance
        """
        user = DysclozurUser.objects.get(user=request.auth.user)
        post = Post()
        post.user = user
        post.date_posted =request.data['date_posted']
        post.title =request.data['title']
        post.text= request.data['text']
        post.link = request.data['link']
        post.url_pic = request.data['url_pic']
        post.url_video = request.data['url_video']
        post.upload_pic = request.data['upload_pic']
        post.upload_video = request.data['upload_video']

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']

class DysclozurUserSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)
    class Meta:
        model = DysclozurUser
        fields = ['user', 'bio', 'avatar']


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    Arguments:
        serializer type
    """
    user = DysclozurUserSerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'user', 'date_posted', 'title', 'text', 'link', 'url_pic', 'url_video', 'upload_pic', 'upload_video', 'flairs')
        depth = 1