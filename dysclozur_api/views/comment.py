from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from dysclozur_api.models import Post, Comment, DysclozurUser, dysclozur_user
from dysclozur_api.views.post import UserSerializer, DysclozurUserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action

class CommentView(ViewSet):
    """DYSCLOZURE POST COMMENTS"""
    def create(self, request):
        # Identify User
        user = User.objects.get(pk=request.auth.user.id)
        #Identify Post
        post = Post.objects.get(pk=request.data['postId'])
        # Create an instance of the comment
        comment = Comment()
        comment.user = user
        comment.post = post
        comment.comment = request.data['comment']

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = User.objects.get(pk=request.auth.user.id)
        post = Post.objects.get(pk=request.data['postId'])

        comment = Comment.objects.get(pk=pk)
        comment.comment = request.data['comment']
        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        post_id = self.request.query_params.get('postId', None) 
        if post_id:
            comments = Comment.objects.filter(post__id=post_id)
        else:
            comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
