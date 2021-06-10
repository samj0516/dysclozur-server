from django.db import models

class Vote(models.Model):
    user = models.ForeignKey('DysclozurUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    upvote = models.BooleanField()