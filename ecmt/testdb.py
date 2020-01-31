# -*- coding: utf-8 -*-
from django.http import HttpResponse
from course.models import courseinfo,teaching,comment
from user.models import UserInfo
from teacher.models import Teacher,Dept
from django.db import connection

# 数据库操作
def test(request):
	insert = courseinfo(course_name='操作系统',deptId=28,course_type='专业必修课程',course_intro='操作系统简介测试')
	insert.save()
	insert = courseinfo(course_name='计算机网络',deptId=28,course_type='专业必修课程',course_intro='计网简介测试')
	insert.save()
	insert = courseinfo(course_name='数据库系统原理',deptId=28,course_type='专业必修课程',course_intro='数据库简介测试')
	insert.save()
	insert = courseinfo(course_name='web应用开发',deptId=28,course_type='专业选修课程',course_intro='web简介测试')
	insert.save()
	insert = courseinfo(course_name='现代CAD技术',deptId=28,course_type='专业选修课程',course_intro='CAD简介测试')
	insert.save()
	return HttpResponse("<p>数据添加成功！</p>")

def test2(request):
	insert = comment(res_id=1,openid='10175102131',score=8.8,comment='操作系统评论测试1')
	insert.save()
	insert = comment(res_id=1,openid='10175102122',score=9.2,comment='操作系统评论测试2')
	insert.save()
	insert = comment(res_id=2,openid='10175102131',score=8.4,comment='计网评论测试1')
	insert.save()
	insert = comment(res_id=2,openid='10175102122',score=8.8,comment='计网评论测试2')
	insert.save()
	insert = comment(res_id=3,openid='10175102131',score=9.1,comment='数据库评论测试')
	insert.save()
	insert = comment(res_id=4,openid='10175102131',score=9.0,comment='web评论测试')
	insert.save()
	insert = comment(res_id=5,openid='10175102131',score=9.2,comment='CAD评论测试')
	insert.save()
	return HttpResponse("<p>数据添加成功！</p>")

def test3(request):
	courseinfo.objects.all().update(deptId=3)
	return HttpResponse("<p>数据修改成功！</p>")

def test4(request):
	insert = teaching(course_id=1,teacher_id=1165)
	insert.save()
	insert = teaching(course_id=1,teacher_id=1202)
	insert.save()
	insert = teaching(course_id=2,teacher_id=1186)
	insert.save()
	insert = teaching(course_id=2,teacher_id=1147)
	insert.save()
	insert = teaching(course_id=3,teacher_id=1192)
	insert.save()
	insert = teaching(course_id=3,teacher_id=1198)
	insert.save()
	insert = teaching(course_id=4,teacher_id=1166)
	insert.save()
	insert = teaching(course_id=5,teacher_id=1165)
	insert.save()
	return HttpResponse("<p>数据添加成功！</p>")

def test5(request):
	insert = comment(res_id=1165,cmt_type='教师',openid='10175102131',score=9.3,comment='李东评论测试1')
	insert.save()
	insert = comment(res_id=1202,cmt_type='教师',openid='10175102122',score=9.5,comment='石亮评论测试1')
	insert.save()
	return HttpResponse("<p>数据添加成功！</p>")