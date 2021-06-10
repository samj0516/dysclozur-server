from django.db import models
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey("DysclozurUser", on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)
    title = models.CharField(max_length=300)
    text = models.TextField(null=True)
    link = models.URLField( null=True)
    url_pic = models.URLField(null=True)
    url_video = models.URLField(null=True)
    upload_pic = models.ImageField(null=True, upload_to='images/', height_field=None, width_field=None)
    upload_video = models.FileField(upload_to='videos/', null=True)
    flairs = models.ManyToManyField('Flair', related_name='posts')
