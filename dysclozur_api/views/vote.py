from dysclozur_api.models.dysclozur_user import DysclozurUser
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth.models import User
from dysclozur_api.models import Vote, Post, 

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'user', 'post', 'upvote' )

class VoteView(ViewSet):
    def list(self, request):
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        user = User.objects.get(pk=request.auth.user.id)
        dysclozur_user = DysclozurUser.objects.get(user=user)
        post = Post.objects.get(pk=request.data['post'])

        vote = Vote()
        vote.post = post
        vote.user = dysclozur_user
        vote.upvote = request.data['upvote']

        try:
            vote.save()
            serializer = VoteSerializer(vote, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)