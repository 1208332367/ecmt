import json
import traceback

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from user.models import UserInfo


@csrf_exempt
def create(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'openid','nick_name','avatar_url'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        user=UserInfo.objects.filter(openid=request.POST['openid'])
        if user.count()>0:
            res = {'code': -3, 'msg': '用户已注册', 'data': []}
        else:
            user=UserInfo.objects.create(**request.POST.dict())
            res['data']={'user_id':user.id}
    except:
        res = {'code': -2, 'msg': 'ServerError', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def get(request):
    res={'code':0, 'msg':'success', 'data':[]}
    try:
        qset=UserInfo.objects.filter(**request.POST.dict())
        if qset.count() == 1:
            res['data'] = json.loads(serializers.serialize("json", qset))[0]['fields']
            res['data']['user_id'] = json.loads(serializers.serialize("json", qset))[0]['pk']

        else:
            res = {'code': -3, 'msg': '用户不存在-3', 'data': []}
    except:
        res = {'code': -2, 'msg': 'ServerError', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))


@csrf_exempt
def update(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        params=request.POST.dict()
        user_id=params['id']
        params.pop('id')
        UserInfo.objects.filter(id=user_id).update(**params)
    except:
        res = {'code': -2, 'msg': 'ServerError', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def login(request):
    res = {'code': -3, 'msg': 'error', 'data': []}
    if  not {'openid'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        qset = UserInfo.objects.filter(**request.POST.dict())
        if qset.count() == 1:
            res = {'code': 0, 'msg': 'success', 'data': {}}
            res['data'] = json.loads(serializers.serialize("json", qset))[0]['fields']
            res['data']['user_id'] = json.loads(serializers.serialize("json", qset))[0]['pk']
    except:
        res = {'code': -2, 'msg': 'ServerError', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))