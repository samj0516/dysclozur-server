from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from dysclozur_api.models import Post, Comment, DysclozurUser
from dysclozur_api.views.post import UserSerializer, DysclozurUserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action

class CommentView(ViewSet):
    """DYSCLOZURE POST COMMENTS"""
    def create(self, request):
        # Identify User
        user = User.objects.get(pk=request.auth.user.id)
        dysclozur_user = DysclozurUser.objects.get(user=user)
        #Identify Post
        post = Post.objects.get(pk=request.data['post'])
        # Create an instance of the comment
        comment = Comment()
        comment.user = dysclozur_user
        comment.post = post
        comment.comment = request.data['comment']

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        

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

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentSerializer(serializers.ModelSerializer):
    user= DysclozurUserSerializer(many=False)
    class Meta:
        model = Comment
        fields =('id', 'user', 'post', 'comment')
        