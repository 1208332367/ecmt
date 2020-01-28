from django.db import models

# Create your models here.
from django.utils import timezone


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    index_url = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    post = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)

class Dept(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)