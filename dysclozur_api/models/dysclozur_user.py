from django.db import models
from django.contrib.auth.models import User

class DysclozurUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, null=True)
    avatar = models.CharField(max_length=300, null=True)