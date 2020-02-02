# -*- coding: utf-8 -*-
import json
import traceback

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from user.models import UserInfo
from course.models import courseinfo,teaching,comment
from teacher.models import Teacher,Dept
from django.db import connection


@csrf_exempt
def listCourse(request):
	request.encoding = 'utf-8'
	res = {'code': -1, 'msg': 'error', 'data': {}}
	try:
		params = request.POST.dict()
		params['status'] = 1
		res['data']['count'] = courseinfo.objects.filter(**params).count()
		res['data']['courses'] = []
		qset = courseinfo.objects.filter(**params)
		ts = json.loads(serializers.serialize("json", qset))
		for t in ts:
			data_row = t['fields']
			data_row['course_id'] = t['pk']
			res['data']['courses'].append(data_row)
		res['code'] = 0
		res['msg'] = 'success'
	except Exception as e:
		res['code'] = -2
		res['msg'] = e
		res['data'] = []
	return HttpResponse(json.dumps(res))

@csrf_exempt
def course_teaching(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	tag = 0
	try:
		current_id = str(request.POST['res_id'])
		res_type = request.POST['res_type']
		cursor=connection.cursor()
		if res_type == '课程':
			res['data']['teachers'] = []
			sql = 'select teacher_id,name,avg_score from teacher_Teacher join course_teaching where teacher_id=teacher_Teacher.id and course_id={} and teacher_Teacher.status=1 and course_teaching.status=1'
			sql2 = sql.format(current_id)
			cursor.execute(sql2)
			qset=cursor.fetchall()
			for i in range(0, len(qset)):
				data_row = {}
				data_row['teacher_id'] = qset[i][0]
				data_row['name'] = qset[i][1]
				data_row['avg_score'] = float(qset[i][2])
				res['data']['teachers'].append(data_row)
			res['code'] = 0
			res['msg'] = 'success'
		elif res_type == '教师':
			res['data']['courses'] = []
			sql = 'select course_courseinfo.course_id,course_name,avg_score from course_courseinfo join course_teaching where course_teaching.course_id=course_courseinfo.course_id and teacher_id={} and course_courseinfo.status=1 and course_teaching.status=1'
			sql2 = sql.format(current_id)
			cursor.execute(sql2)
			qset=cursor.fetchall()
			for i in range(0, len(qset)):
				data_row = {}
				data_row['course_id'] = qset[i][0]
				data_row['name'] = qset[i][1]
				data_row['avg_score'] = float(qset[i][2])
				res['data']['courses'].append(data_row)
			res['code'] = 0
			res['msg'] = 'success'
		else:
			res = {'code': -1, 'msg': 'res_type error！', 'data': []}
	except Exception as e:
		res = {'code': -2, 'msg': e, 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def more_comment(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	tag = 0
	resName = ''
	try:
		current_id = request.POST['res_id']
		typeof_cmt = request.POST['res_type']
		res['data']['comment_info'] = []
		if typeof_cmt == '课程':
			qset = courseinfo.objects.filter(course_id=current_id,status=1)
			DATA = json.loads(serializers.serialize("json", qset))
			resName = DATA[0]['fields']['course_name']
		elif typeof_cmt == '教师':
			qset = Teacher.objects.filter(id=current_id,status=1)
			DATA = json.loads(serializers.serialize("json", qset))
			resName = DATA[0]['fields']['name']
		else:
			tag = -2
		if len(qset)>0:
			cursor=connection.cursor()
			sql = 'select comment_id,user_userinfo.openid,user_userinfo.avatar_url,nick_name,stars,comment,score,approve_num,oppose_num,course_comment.mtime from user_userinfo join course_comment where user_userinfo.openid=course_comment.openid and res_id={} and cmt_type="{}" and course_comment.status=1 and user_userinfo.status=1 order by course_comment.mtime desc'
			sql2 = sql.format(current_id,typeof_cmt)
			cursor.execute(sql2)
			qset = cursor.fetchall()
			if len(qset)>0:
				for i in range(0, len(qset)):
					tmp = {}
					tmp['resName'] = resName
					tmp['cmt_type'] = typeof_cmt
					tmp['comment_id'] = qset[i][0]
					tmp['user_id'] = qset[i][1]
					tmp['avatar'] = qset[i][2]
					tmp['name'] = qset[i][3]
					tmp['star'] = qset[i][4]
					tmp['des'] = qset[i][5]
					tmp['score'] = qset[i][6]
					tmp['agree'] = qset[i][7]
					tmp['disagree'] = qset[i][8]
					tmp['date'] = str(qset[i][9].year)+"年"+str(qset[i][9].month)+"月"+str(qset[i][9].day)+"日"
					str1 = str(qset[i][9].hour)
					str2 = str(qset[i][9].minute)
					if qset[i][9].hour < 10:
						str1 = "0"+str1
					if qset[i][9].minute < 10:
						str2 = "0"+str2
					tmp['time'] = str1+":"+str2
					res['data']['comment_info'].append(tmp)
			else:
				tag = -1
			if tag == -1:
				res['code'] = -1
				res['msg'] = '无该课程或教师评论记录！'
			else:
				res['code'] = 0
				res['msg'] = 'success'
		else:
			if tag == -2:
				res = {'code': -1, 'msg': 'cmt_type error', 'data': []}
			else:
				res = {'code': -2, 'msg': '无该课程或教师数据记录！', 'data': []}
	except Exception as e:
		res = {'code': -3, 'msg': e, 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))



@csrf_exempt
def submit_comment(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	tag = 0
	try:
		current_id = str(request.POST['res_id'])
		typeof_cmt = request.POST['res_type']
		user_id = request.POST['user_id'].strip()
		submit_score = float(request.POST['score'].strip())
		submit_comment = request.POST['comment'].strip()
		if typeof_cmt == '课程':
			qset = courseinfo.objects.filter(course_id=current_id,status=1)
		elif typeof_cmt == '教师':
			qset = Teacher.objects.filter(id=current_id,status=1)
		else:
			tag = -2
		if len(qset)==1:
			DATA = json.loads(serializers.serialize("json", qset))
			if abs(submit_score-float(DATA[0]['fields']['avg_score']))>2:
				res = {'code':-1, 'msg':'您的打分被系统判定为无效，请重新打分！', 'data':[]}
				return HttpResponse(json.dumps(res))
			else:
				insert = comment(res_id=current_id,cmt_type=typeof_cmt,openid=user_id,score=submit_score,comment=submit_comment)
				insert.save()
				sum_userstar = 0
				sum_score = 0.0
				cursor=connection.cursor()
				sql = 'select stars,score from user_userinfo join course_comment where user_userinfo.openid=course_comment.openid and res_id={} and cmt_type="{}"'
				sql2 = sql.format(current_id,typeof_cmt)
				cursor.execute(sql2)
				qset=cursor.fetchall()
				for i in range(0, len(qset)):
					sum_score = sum_score + qset[i][0]*qset[i][1]
					sum_userstar = sum_userstar + qset[i][0]
				new_avgscore = round(sum_score/sum_userstar, 2)
				if typeof_cmt == '课程':
					courseinfo.objects.filter(course_id=current_id).update(avg_score=new_avgscore,cmt_cnt=len(qset))
				else:
					Teacher.objects.filter(id=current_id).update(avg_score=new_avgscore,cmt_cnt=len(qset))
				res = {'code': 0, 'msg': '评价成功！', 'data': []}
		else:
			if tag == -2:
				res = {'code': -1, 'msg': 'cmt_type error', 'data':[]}
			else:
				res = {'code': -2, 'msg': '无该课程或教师数据记录！', 'data': []}
	except Exception as e:
		res = {'code': -3, 'msg': e, 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def favor_comment(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	tag = 0
	try:
		coursecmt_id = int(request.POST['comment_id'].strip())
		isfavor_coursecmt = int(request.POST['isfavor_coursecmt'].strip())
		isoppose_coursecmt = int(request.POST['isoppose_coursecmt'].strip())
		qset = comment.objects.filter(comment_id=coursecmt_id)
		if len(qset)==1:
			DATA = json.loads(serializers.serialize("json", qset))
			current_approve = DATA[0]['fields']['approve_num'] + isfavor_coursecmt
			current_oppose = DATA[0]['fields']['oppose_num'] + isoppose_coursecmt
			comment.objects.filter(comment_id=coursecmt_id).update(approve_num=current_approve,oppose_num=current_oppose)
			res = {'code': 0, 'msg': 'success', 'data': []}
		else:
			res = {'code': -1, 'msg': '评论不存在！', 'data': []}
	except Exception as e:
		res = {'code': -2, 'msg': e, 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def hot_comment(request):
	request.encoding = 'utf-8'
	res = {'code':0, 'msg':'success', 'data':{}}
	res['data']['comment_info'] = []
	try:
		comment_type = request.POST['cmt_type'].strip()
		cursor=connection.cursor()
		if comment_type == '课程' or comment_type == '所有':
			sql = 'select comment_id,res_id,course_courseinfo.course_name,user_userinfo.openid,user_userinfo.avatar_url,nick_name,stars,comment,score,cmt_type,approve_num,oppose_num,course_comment.mtime from (user_userinfo join course_comment) join course_courseinfo where course_comment.res_id=course_courseinfo.course_id and user_userinfo.openid=course_comment.openid and cmt_type="课程" and course_courseinfo.status=1 and course_comment.status=1 and user_userinfo.status=1 order by course_comment.mtime desc'
			cursor.execute(sql)
			qset = cursor.fetchall()
			if len(qset)>0:
				for i in range(0, len(qset)):
					tmp = {}
					tmp['comment_id'] = qset[i][0]
					tmp['res_id'] = qset[i][1]
					tmp['resName'] = qset[i][2]
					tmp['user_id'] = qset[i][3]
					tmp['avatar'] = qset[i][4]
					tmp['name'] = qset[i][5]
					tmp['star'] = qset[i][6]
					tmp['des'] = qset[i][7]
					tmp['score'] = qset[i][8]
					tmp['cmt_type'] = qset[i][9]
					tmp['agree'] = qset[i][10]
					tmp['disagree'] = qset[i][11]
					tmp['date'] = str(qset[i][12].year)+"年"+str(qset[i][12].month)+"月"+str(qset[i][12].day)+"日"
					str1 = str(qset[i][12].hour)
					str2 = str(qset[i][12].minute)
					if qset[i][12].hour < 10:
						str1 = "0"+str1
					if qset[i][12].minute < 10:
						str2 = "0"+str2
					tmp['time'] = str1+":"+str2
					res['data']['comment_info'].append(tmp)
				res['code'] = 0
				res['msg'] = 'success'	
			else:
				res = {'code': -1, 'msg': '当前分类无任何热评！', 'data': []}
		if comment_type == '教师' or comment_type == '所有':
			sql = 'select comment_id,res_id,teacher_Teacher.name,user_userinfo.openid,user_userinfo.avatar_url,nick_name,stars,comment,score,cmt_type,approve_num,oppose_num,course_comment.mtime from (user_userinfo join course_comment) join teacher_Teacher where course_comment.res_id=teacher_Teacher.id and user_userinfo.openid=course_comment.openid and cmt_type="教师" and course_comment.status=1 and user_userinfo.status=1 and teacher_Teacher.status=1 order by course_comment.mtime desc'
			cursor.execute(sql)
			qset = cursor.fetchall()
			if len(qset)>0:
				for i in range(0, len(qset)):
					tmp = {}
					tmp['comment_id'] = qset[i][0]
					tmp['res_id'] = qset[i][1]
					tmp['resName'] = qset[i][2]
					tmp['user_id'] = qset[i][3]
					tmp['avatar'] = qset[i][4]
					tmp['name'] = qset[i][5]
					tmp['star'] = qset[i][6]
					tmp['des'] = qset[i][7]
					tmp['score'] = qset[i][8]
					tmp['cmt_type'] = qset[i][9]
					tmp['agree'] = qset[i][10]
					tmp['disagree'] = qset[i][11]
					tmp['date'] = str(qset[i][12].year)+"年"+str(qset[i][12].month)+"月"+str(qset[i][12].day)+"日"
					res['data']['comment_info'].append(tmp)	
				res['code'] = 0
				res['msg'] = 'success'
			else:
				res = {'code': -1, 'msg': '当前分类无任何热评！', 'data': []}
	except Exception as e:
		res = {'code': -2, 'msg': e, 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))