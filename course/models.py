from django.db import models
from django.utils import timezone
# Create your models here.
 
class courseinfo(models.Model):
	course_id = models.AutoField(primary_key=True)
	course_name = models.CharField(max_length=200,default='')
	deptId = models.IntegerField(default=1)
	course_type = models.CharField(max_length=100,default='')
	course_intro = models.CharField(max_length=500,default='')
	avg_score = models.DecimalField(max_digits=5, decimal_places=2,default=8.0)
	cmt_cnt = models.IntegerField(default=0)
	status = models.IntegerField(default=1)
	ctime = models.DateTimeField(default = timezone.now)
	mtime = models.DateTimeField(auto_now = True)

class teaching(models.Model):
	course_id = models.IntegerField(default=1)
	teacher_id = models.IntegerField(default=1)
	status = models.IntegerField(default=1)
	ctime = models.DateTimeField(default = timezone.now)
	mtime = models.DateTimeField(auto_now = True)

class comment(models.Model):
	comment_id = models.AutoField(primary_key=True)
	res_id = models.IntegerField(default=1)
	cmt_type = models.CharField(max_length=10,default='课程')
	openid = models.CharField(max_length=100)
	score = models.FloatField(default=8.0)
	comment = models.CharField(max_length=1000,default='')
	approve_num = models.IntegerField(default=0)
	oppose_num = models.IntegerField(default=0)
	status = models.IntegerField(default=1)
	ctime = models.DateTimeField(default = timezone.now)
	mtime = models.DateTimeField(auto_now = True)