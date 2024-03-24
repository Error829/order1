import random
import datetime

from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.shortcuts import render, redirect, reverse

from web import models
from Order1 import settings
from utils.BaseResponse import BaseResponse
from utils.pagination import Pagination
from utils.video import get_old_view_count
from web.modelforms.order import OrderAddModel
from web.modelforms.customer import CustomerTradeModel


def order(request):
    form = OrderAddModel(request)
    querylist = models.Order.objects.filter(customer_id=request.user_object.user_id).order_by('-id')
    pagination_object = Pagination(request, querylist)
    content = {'querylist': querylist[pagination_object.start: pagination_object.end],
               'paramstring': pagination_object.get_paramstring(),
               'form': form}
    return render(request, 'order.html', locals())


def order_add(request):
    if request.method == 'GET':
        form = OrderAddModel(request)
        return render(request, 'order_add.html', {'form': form})
    form = OrderAddModel(request, data=request.POST)
    if not form.is_valid():
        return render(request, 'order_add.html', {'form': form})
    # 检验通过 说明一切数据都合法了准备开始生成订单以及交易记录
    # 获取视频url 和数量
    video_url = form.cleaned_data['url']
    count = form.cleaned_data['count']
    try:
        with transaction.atomic():
            cus_object = models.Customer.objects.filter(id=request.user_object.user_id).select_for_update().first()
            # 根据视频url 获取视频原播放量
            status, old_view_count = get_old_view_count(video_url)
            if not status:
                form.add_error('url', "视频原播放获取失败")
                return render(request, 'order_add.html', {"form": form})
            # 生成一个随机不重复的订单号并生成订单
            while True:
                rand_number = random.randint(10000, 99999)
                ctime = datetime.datetime.now().strftime("%Y%m%d")
                oid = "{}{}".format(ctime, rand_number)
                exists = models.Order.objects.filter(oid=oid).exists()
                if exists:
                    continue
                break
            form.instance.status = 1
            form.instance.oid = oid
            form.instance.customer_id = request.user_object.user_id
            form.instance.price = form.price
            form.instance.real_price = form.real_price
            form.instance.old_view_count = old_view_count
            form.save()
            # 根据form 对象中的real_price进行扣款
            real_price = form.real_price
            # models.Customer.objects.filter(id=request.user_object.user_id).update(balance=F('balance') - real_price)
            cus_object.balance -= real_price
            cus_object.save()
            # 生成交易记录
            models.TransactionRecord.objects.create(
                charge_type=3,
                customer_id=request.user_object.user_id,
                amount=real_price,
                order_oid=oid,
            )
            # 写入redis队列
            conn = get_redis_connection("default")
            conn.lpush(settings.ORDER_TASK_NAME, oid)
    except Exception as e:
        form.add_error('count', '创建订单失败')
        print(e)
        return render(request, 'order_add.html', {'form': form})

    return redirect(reverse('order'))


def order_list(request):
    form = CustomerTradeModel()

    keyword = request.GET.get("keyword", "").strip()
    con = Q()
    if keyword:
        con.connector = 'OR'
        con.children.append(('order_oid__contains', keyword))

    querylist = models.TransactionRecord.objects.filter(con).filter(customer_id=request.user_object.user_id,
                                                                    customer_id__active=1,
                                                                    active=1).order_by('-id')
    pagination_object = Pagination(request, querylist)
    content = {'querylist': querylist[pagination_object.start: pagination_object.end],
               'paramstring': pagination_object.get_paramstring(),
               'form': form,
               'customer_id': request.user_object.user_id, }
    return render(request, 'order_list.html', content)


def order_cancel(request):
    # 获取当前用户,订单对象
    res = BaseResponse()
    user_obj = models.Customer.objects.filter(id=request.user_object.user_id, active=1).first()
    order_oid = request.POST.get('order_oid', '')
    if not order_oid:
        res.status = False
        res.detail = '订单不存在'
        return JsonResponse(res.dict)
    try:
        with transaction.atomic():
            order_obj = models.Order.objects.filter(customer_id=request.user_object.user_id,
                                                    oid=order_oid,
                                                    active=1).select_for_update().first()
            # 1.更改状态为5-已撤单(ajax请求把订单号发过来)
            order_obj.status = 5
            order_obj.save()
            # 2.查询该订单费用并返还费用
            fee = order_obj.real_price
            user_obj.balance += fee
            user_obj.save()
            # 3.生成交易记录
            models.TransactionRecord.objects.create(
                charge_type=5,
                customer_id=request.user_object.user_id,
                amount=fee,
                order_oid=order_oid,
            )
    except Exception as e:
        print(e)
        res.status = False
        res.detail = '撤单出错'
        return JsonResponse(res.dict)
    res.status = True
    return JsonResponse(res.dict)
