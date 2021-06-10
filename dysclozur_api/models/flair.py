from django.db import models

class Flair(models.Model):
    label = models.CharField(max_length=80)