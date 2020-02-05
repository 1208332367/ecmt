import json
import traceback

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from teacher.models import Teacher, Dept


@csrf_exempt
def listTeacher(request):
    res = {'code': -1, 'msg': 'error', 'data': {}}
    try:
        params = request.POST.dict()
        params['status'] = 1
        res['data']['count'] = Teacher.objects.filter(**params).count()
        res['data']['teachers'] = []
        qset = Teacher.objects.filter(**params)
        ts = json.loads(serializers.serialize("json", qset))
        for t in ts:
            data_row = t['fields']
            data_row['id'] = t['pk']
            res['data']['teachers'].append(data_row)
        res['code'] = 0
        res['msg'] = 'success'
    except Exception as e:
        res['code'] = -2
        res['msg'] = e
        res['data'] = []
    return HttpResponse(json.dumps(res))

@csrf_exempt
def listDept(request):
    res = {'code': -1, 'msg': 'error', 'data': {}}
    try:
        params = request.POST.dict()
        params['status'] = 1
        res['data']['count'] = Dept.objects.filter(**params).count()
        res['data']['depts'] = []
        qset = Dept.objects.filter(**params)
        ts = json.loads(serializers.serialize("json", qset))
        for t in ts:
            data_row = t['fields']
            data_row['id'] = t['pk']
            res['data']['depts'].append(data_row)
        res['code']=0
        res['msg']='success'
    except Exception as e:
        res['code'] = -2
        res['msg'] = e
        res['data'] = []
    return HttpResponse(json.dumps(res))