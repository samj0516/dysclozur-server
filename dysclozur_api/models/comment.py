from django.db import models

class Comment(models.Model):
    user = models.ForeignKey('DysclozurUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.TextField(default="")