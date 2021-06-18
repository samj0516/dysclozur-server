from dysclozur_api.models.dysclozur_user import DysclozurUser
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth.models import User
from dysclozur_api.models import Vote, Post, Flair

class FlairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flair
        fields = ('id', 'label')

class FlairView(ViewSet):
    def list(self, request):
        flairs = Flair.objects.all()
        serializer = FlairSerializer(flairs, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        flair = Flair()
        flair.label = request.data['label']