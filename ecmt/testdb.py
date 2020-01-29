# -*- coding: utf-8 -*-
from django.http import HttpResponse
from course.models import courseinfo,teaching,comment
from user.models import UserInfo

# 数据库操作
def test(request):
	insert = courseinfo(course_name='操作系统',course_type='专业必修课程',course_intro='操作系统简介测试',avg_score=9.3,cmt_num=1)
	insert.save()
	insert = courseinfo(course_name='计算机网络',course_type='专业必修课程',course_intro='计网简介测试',avg_score=8.8,cmt_num=1)
	insert.save()
	insert = courseinfo(course_name='数据库系统原理',course_type='专业必修课程',course_intro='数据库简介测试',avg_score=9.4,cmt_num=1)
	insert.save()
	insert = courseinfo(course_name='web应用开发',course_type='专业选修课程',course_intro='web简介测试',avg_score=9.6,cmt_num=1)
	insert.save()
	insert = courseinfo(course_name='现代CAD技术',course_type='专业选修课程',course_intro='CAD简介测试',avg_score=9.2,cmt_num=1)
	insert.save()
	return HttpResponse("<p>数据添加成功！</p>")

def test2(request):
	insert = comment(res_id=1,openid='10175102131',score=9.3,comment='操作系统评论测试')
	insert.save()
	insert = comment(res_id=1,openid='10175102122',score=9.5,comment='操作系统评论测试22')
	insert.save()
	insert = comment(res_id=2,openid='10175102131',score=8.8,comment='计网评论测试')
	insert.save()
	insert = comment(res_id=2,openid='10175102122',score=8.5,comment='计网评论测试22')
	insert.save()
	insert = comment(res_id=3,openid='10175102131',score=9.4,comment='数据库评论测试')
	insert.save()
	insert = comment(res_id=4,openid='10175102131',score=9.6,comment='web评论测试')
	insert.save()
	insert = comment(res_id=5,openid='10175102131',score=9.2,comment='CAD评论测试')
	insert.save()
	return HttpResponse("<p>数据添加成功！</p>")

def test3(request):
	comment.objects.all().update(comment='操作系统评论测试2')
	return HttpResponse("<p>数据修改成功！</p>")

def test4(request):
	insert = teaching(course_id=1,teacher='李东')
	insert.save()
	insert = teaching(course_id=1,teacher='石亮')
	insert.save()
	insert = teaching(course_id=1,teacher='诸葛晴凤')
	insert.save()
	insert = teaching(course_id=2,teacher='黄新力')
	insert.save()
	insert = teaching(course_id=2,teacher='陆刚')
	insert.save()
	insert = teaching(course_id=3,teacher='徐飞')
	insert.save()
	insert = teaching(course_id=3,teacher='孙蕾')
	insert.save()
	insert = teaching(course_id=4,teacher='张倩')
	insert.save()
	insert = teaching(course_id=5,teacher='李东')
	insert.save()
	return HttpResponse("<p>数据添加成功！</p>")