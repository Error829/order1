import os
import sys
import random

from django.conf import settings
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.shortcuts import render, redirect, HttpResponse

from web import models
from utils.sendsms import smssend
from utils.BaseResponse import BaseResponse
from web.forms.login import LoginForm, SmsLoginForm, MobileForm

BASEPATH = os.path.dirname(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(BASEPATH)


class ROLE(object):
    CUSTOMER = '1'
    ADMIN = '2'


def logout(request):
    request.session.clear()
    return redirect(settings.LOGIN_HOME)


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {'form': form})

    # 检验数据有无空数据
    form = LoginForm(data=request.POST)

    if not form.is_valid():
        return render(request, "login.html", {'form': form})
    # 获取数据信息去数据库比对
    data_dict = form.cleaned_data
    role = data_dict.pop('role')

    # 去数据库中进行数据比对
    if role == ROLE.ADMIN:
        user_object = models.Administrator.objects.filter(active=1).filter(**data_dict).first()
    else:
        user_object = models.Customer.objects.filter(active=1).filter(**data_dict).first()
    if not user_object:
        return render(request, "login.html", {'form': form, 'error': '用户名或密码不存在'})

    # 用户登录信息写入session做记录 + 进入后台
    mapping = {"1": "CUSTOMER", "2": "ADMIN"}
    request.session[settings.ORDER_USER_INFO] = {'user_id': user_object.pk, 'role': mapping[role],
                                                 'username': user_object.username,
                                                 'password': user_object.password}

    return redirect(settings.LOGIN_HOME)


def sms_login(request):
    if request.method == 'GET':
        form = SmsLoginForm()
        return render(request, "sms_login.html", {'form': form})

    res = BaseResponse()
    # 拿到post数据
    form = SmsLoginForm(data=request.POST)
    # form校验+返回报错信息
    if not form.is_valid():
        res.detail = form.errors
        return JsonResponse(res.dict, json_dumps_params={"ensure_ascii": False})
    # redis取值校验
    conn = get_redis_connection("default")
    moblie = form.cleaned_data['mobile']
    code = form.cleaned_data['code']

    try:
        redis_code = conn.get(moblie)
        redis_code = redis_code.decode('utf-8')
    except Exception as e:
        res.detail = {'code': ['未获取验证码']}
        return JsonResponse(res.dict, json_dumps_params={"ensure_ascii": False})

    if code != redis_code:
        res.detail = {'code': ['验证码错误']}
        return JsonResponse(res.dict, json_dumps_params={"ensure_ascii": False})
    # 数据库存在校验
    role = form.cleaned_data['role']
    if role == ROLE.ADMIN:
        user_object = models.Administrator.objects.filter(active=1, mobile=moblie).first()
    else:
        user_object = models.Customer.objects.filter(active=1, mobile=moblie).first()
    if not user_object:
        res.detail = {'mobile': ["该用户不存在"]}
        return JsonResponse(res.dict, json_dumps_params={"ensure_ascii": False})
    # 跳转
    # 用户登录信息写入session做记录 + 进入后台
    mapping = {"1": "CUSTOMER", "2": "ADMIN"}
    request.session['user_info'] = {'role': mapping[role], 'username': user_object.username,
                                    'password': user_object.password}
    res.status = True
    res.data = settings.LOGIN_HOME
    return JsonResponse(res.dict, json_dumps_params={"ensure_ascii": False})


def sms_send(request):
    # 1.获取手机号 检验手机号
    if request.method == 'GET':
        return HttpResponse('非法请求')
    form = MobileForm(data=request.POST)
    # print(request.POST)
    res = BaseResponse()
    if not form.is_valid():
        # print(form.errors)
        res.detail = form.errors
        return JsonResponse(res.dict, json_dumps_params={"ensure_ascii": False})
    moblie_number = form.cleaned_data['mobile']
    # 2.生成验证码 发送验证码
    code_send = str(random.randint(1000, 9999))
    content = '您的验证码为{},60s有效'.format(code_send)
    tip = smssend(content, moblie_number)
    if tip != '短信发送成功':
        res.detail = {'mobile': [tip, ]}
        return JsonResponse(res.dict, json_dumps_params={"ensure_ascii": False})
    # 3.存储手机号及验证码到redis 设置超时时间
    conn = get_redis_connection("default")
    conn.set(moblie_number, code_send, ex=60)
    # 4.用户输入信息进行比对登录
    res.status = True
    res.data = settings.LOGIN_HOME
    return JsonResponse(res.dict)


def home(request):
    return render(request, 'home.html')
