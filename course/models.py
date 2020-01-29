from django.db import models
from django.utils import timezone
# Create your models here.
 
class courseinfo(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50,default='')
    course_type = models.CharField(max_length=50,default='')
    course_intro = models.CharField(max_length=500,default='')
    avg_score = models.FloatField(default=0.0)
    cmt_num = models.IntegerField(default=0)

class teaching(models.Model):
	course_id = models.IntegerField(default=0)
	teacher = models.CharField(max_length=20,default='')

class comment(models.Model):
	comment_id = models.AutoField(primary_key=True)
	res_id = models.IntegerField(default=0)
	cmt_type = models.CharField(max_length=10,default='课程')
	ctime = models.DateTimeField(default = timezone.now)
	mtime = models.DateTimeField(auto_now = True)
	openid = models.CharField(max_length=100)
	score = models.FloatField(default=0.0)
	comment = models.CharField(max_length=500,default='')
	approve_num = models.IntegerField(default=0)
	oppose_num = models.IntegerField(default=0)