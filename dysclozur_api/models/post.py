from django.db import models
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey("DysclozurUser", on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=300)
    text = models.TextField(null=True)
    link = models.URLField( null=True)
    url_pic = models.URLField(null=True)
    url_video = models.URLField(null=True)
    upload_pic = models.URLField(null=True)
    upload_video = models.URLField(null=True)
    flairs = models.ManyToManyField('Flair', related_name='posts')
