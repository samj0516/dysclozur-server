from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from dysclozur_api.models import Post, DysclozurUser, Flair
from django.contrib.auth.models import User
from rest_framework.decorators import action
import cloudinary
from django.conf import settings
import environ
env = environ.Env()
environ.Env.read_env()




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
        # cloudinary.config(cloud_name='dysclozur',
        #         api_key=env('CLOUDINARY_API_KEY'),
        #         api_secret=env('CLOUDINARY_SECRET_KEY'))
        cloudinary.config(cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
                  api_key=int(settings.CLOUDINARY_STORAGE['API_KEY']),
                  api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'])

        user = DysclozurUser.objects.get(user=request.auth.user)
        post = Post()
        post.user = user
        post.date_posted =request.data['date_posted']
        post.title =request.data['title']
        post.text= request.data['text']
        post.link = request.data['link']
        post.url_pic = request.data['url_pic']
        post.url_video = request.data['url_video']
        if request.data['upload_pic'] == None:
            post.upload_pic = None
        else:
            upload_pic =  cloudinary.uploader.upload(request.data['upload_pic'], folder='dysclozurImages', format='jpg')
            post.upload_pic = upload_pic['url']
        if request.data['upload_video'] == None:
            post.upload_video = None
        else:
            upload_video = cloudinary.uploader.upload(request.data['upload_video'], folder='dysclozurVideo', resource_type = 'video', quality = "auto")
            post.upload_video = upload_video['url']
        

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post
        Returns:
            Response -- JSON serialized post instance
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Hnalde PUT requests for post
        Returns:
            Response -- Empty body with 204 status code
        """
        cloudinary.config(cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
                  api_key=int(settings.CLOUDINARY_STORAGE['API_KEY']),
                  api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'])
                  
        user = DysclozurUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        post.user = user
        post.date_posted = request.data['date_posted']
        post.title = request.data['title']
        post.text = request.data['text']
        post.link = request.data['link']
        post.url_pic = request.data['url_pic']
        post.url_video = request.data['url_video']
        if request.data['upload_pic'] == None:
            post.upload_pic = None
        else:
            upload_pic =  cloudinary.uploader.upload(request.data['upload_pic'], folder='dysclozurImages', format='jpg')
            post.upload_pic = upload_pic['url']
        if request.data['upload_video'] == None:
            post.upload_video = None
        else:
            upload_video = cloudinary.uploader.upload(request.data['upload_video'], folder='dysclozurVideo', resource_type = 'video', quality = "auto")
            post.upload_video = upload_video['url']
        
        post.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def flair(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        flair = Flair.objects.get(pk=request.data['flairId'])
        if request.method == "POST":
            try:
                post.flairs.add(flair)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception:
                return HttpResponse(Exception)
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
        depth = 2