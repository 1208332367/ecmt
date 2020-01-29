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
from django.db import connection


@csrf_exempt
def type_select(request):
	request.encoding = 'utf-8'
	res = {'code':0, 'msg':'success', 'data':[]}
	try:
		typeof_course = request.POST['course_type'].strip()
		qset = courseinfo.objects.filter(course_type=typeof_course)
		if len(qset)>0:
			ALL_DATA = json.loads(serializers.serialize("json", qset))
			selected_data = []
			for i in range(0, len(ALL_DATA)):
				selected_data.append(ALL_DATA[i]['fields']['course_name'])
			res = {'code': 0, 'msg': '操作成功！', 'data': selected_data}
		else:
			res = {'code': -1, 'msg': '无该类别课程数据记录！', 'data': []}
	except:
		res = {'code': -2, 'msg': '操作异常！', 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def course_select(request):
	request.encoding = 'utf-8'
	res = {'code':0, 'msg':'success', 'data':[]}
	try:
		typeof_course = request.POST['course_type'].strip()
		nameof_course = request.POST['course_name'].strip()
		qset = courseinfo.objects.filter(course_type=typeof_course,course_name=nameof_course)
		if len(qset)==1:
			DATA = json.loads(serializers.serialize("json", qset))
			res['data'].append(DATA[0]['fields'])
			current_id = DATA[0]['pk']
			cursor=connection.cursor()
			sql = 'select nick_name,avatar_url,score,comment,approve_num,oppose_num from user_userinfo join course_comment where user_userinfo.openid=course_comment.openid and res_id={} and cmt_type="课程" order by course_comment.mtime desc limit 1'
			sql2 = sql.format(current_id)
			cursor.execute(sql2)
			qset=cursor.fetchall()
			if len(qset)==1:
				dict_trans = [{'nick_name':qset[0][0],'avatar_url':qset[0][1],'score':qset[0][2],'comment':qset[0][3],'approve_num':qset[0][4],'oppose_num':qset[0][5]}]
				res['data'].append(dict_trans)
			else:
				msg = '无该课程评论记录！'
			qset = teaching.objects.filter(course_id=current_id)
			DATA = json.loads(serializers.serialize("json", qset))
			for i in range(0, len(DATA)):
				res['data'].append(DATA[i]['fields']['teacher'])
			res['msg'] = '操作成功！'
		else:
			res = {'code': -1, 'msg': '无该课程数据记录！', 'data': []}
	except:
		res = {'code': -2, 'msg': '操作异常！', 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def more_coursecmt(request):
	request.encoding = 'utf-8'
	res = {'code':0, 'msg':'success', 'data':[]}
	try:
		typeof_course = request.POST['course_type'].strip()
		nameof_course = request.POST['course_name'].strip()
		qset = courseinfo.objects.filter(course_type=typeof_course,course_name=nameof_course)
		if len(qset)==1:
			DATA = json.loads(serializers.serialize("json", qset))
			course_id = DATA[0]['pk']
			cursor=connection.cursor()
			sql = 'select comment_id,nick_name,avatar_url,score,comment,approve_num,oppose_num from user_userinfo join course_comment where user_userinfo.openid=course_comment.openid and res_id={} and cmt_type="课程" order by course_comment.mtime desc'
			sql2 = sql.format(course_id)
			cursor.execute(sql2)
			qset=cursor.fetchall()
			if len(qset)>0:
				dict_trans = []
				for i in range(0, len(qset)):
					dict_trans.append([{'comment_id':qset[i][0],'nick_name':qset[i][1],'avatar_url':qset[i][2],'score':qset[i][3],'comment':qset[i][4],'approve_num':qset[i][5],'oppose_num':qset[i][6]}])
				res['data'] = dict_trans
				res['msg'] = '操作成功！'
			else:
				msg = '无该课程评论记录！'
		else:
			res = {'code': -1, 'msg': '无该课程数据记录！', 'data': []}
	except:
		res = {'code': -2, 'msg': '操作异常！', 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def submit_coursecmt(request):
	request.encoding = 'utf-8'
	res = {'code':0, 'msg':'success', 'data':[]}
	try:
		typeof_course = request.POST['course_type'].strip()
		nameof_course = request.POST['course_name'].strip()
		user_id = request.POST['user_id'].strip()
		submit_score = float(request.POST['score'].strip())
		submit_comment = request.POST['comment'].strip()
		qset = courseinfo.objects.filter(course_type=typeof_course,course_name=nameof_course)
		if len(qset)==1:
			DATA = json.loads(serializers.serialize("json", qset))
			current_id = DATA[0]['pk']
			if abs(submit_score-DATA[0]['fields']['avg_score'])>2:
				res = {'code':-1, 'msg':'您的打分被系统判定为无效，请重新打分！', 'data':[]}
				return HttpResponse(json.dumps(res))
			else:
				insert = comment(res_id=current_id,openid=user_id,score=submit_score,comment=submit_comment)
				insert.save()
				comment_num = DATA[0]['fields']['cmt_num'] + 1
				courseinfo.objects.filter(course_id=current_id).update(cmt_num=comment_num)
				sum_userstar = 0
				sum_score = 0.0
				cursor=connection.cursor()
				sql = 'select status,score from user_userinfo join course_comment where user_userinfo.openid=course_comment.openid and res_id={} and cmt_type="课程"'
				sql2 = sql.format(current_id)
				cursor.execute(sql2)
				qset=cursor.fetchall()
				for i in range(0, len(qset)):
					sum_score = sum_score + qset[i][0]*qset[i][1]
					sum_userstar = sum_userstar + qset[i][0]
				new_avgscore = round(sum_score/sum_userstar, 1)
				courseinfo.objects.filter(course_id=current_id).update(avg_score=new_avgscore)
				res = {'code': 0, 'msg': '课程评价成功！', 'data': []}
		else:
			res = {'code': -2, 'msg': '课程不存在！', 'data': []}
	except:
		res = {'code': -3, 'msg': '操作异常！', 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def course_favorcmt(request):
	request.encoding = 'utf-8'
	res = {'code':0, 'msg':'success', 'data':[]}
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
			res = {'code': 0, 'msg': '操作成功！', 'data': []}
		else:
			res = {'code': -1, 'msg': '评论不存在！', 'data': []}
	except:
		res = {'code': -2, 'msg': '操作异常！', 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def course_hotcmt(request):
	request.encoding = 'utf-8'
	res = {'code':0, 'msg':'success', 'data':[]}
	try:
		comment_type = request.POST['cmt_type'].strip()
		qset = comment.objects.filter(cmt_type=comment_type)
		if len(qset)>0:
			ALL_DATA = json.loads(serializers.serialize("json", qset))
			selected_data = []
			for i in range(0, len(ALL_DATA)):
				ALL_DATA[i]['fields']['comment_id'] = ALL_DATA[i]['pk']
				selected_data.append(ALL_DATA[i]['fields'])
			res = {'code': 0, 'msg': '操作成功！', 'data': selected_data}
		else:
			res = {'code': -1, 'msg': '无任何课程热评！', 'data': []}
	except:
		res = {'code': -2, 'msg': '操作异常！', 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))