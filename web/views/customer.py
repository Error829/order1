from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from django.db import transaction
from django.shortcuts import redirect, render

from web import models
from utils.BaseResponse import BaseResponse
from utils.pagination import Pagination
from web.modelforms.customer import CustomerForm, CustomerEditForm, CustomerPasswordForm, CustomerTradeModel


def customer(request):
    keyword = request.GET.get("keyword", "").strip()
    con = Q()
    if keyword:
        con.connector = 'OR'
        con.children.append(('username__contains', keyword))
        con.children.append(('mobile__contains', keyword))
        con.children.append(('level__title__contains', keyword))

    querylist = models.Customer.objects.filter(con).filter(active=1).select_related('level', 'creator')
    pagination_object = Pagination(request, querylist)
    content = {'querylist': querylist[pagination_object.start: pagination_object.end],
               'paramstring': pagination_object.get_paramstring()}
    return render(request, 'customer.html', content)


def customer_add(request):
    if request.method == 'GET':
        form = CustomerForm(request)
        return render(request, 'customer_add.html', {'form': form})
    form = CustomerForm(request, data=request.POST)
    if not form.is_valid():
        return render(request, 'customer_add.html', {'form': form})
    form.instance.creator_id = request.user_object.user_id
    form.save()
    return redirect(reverse('customer'))


def customer_edit(request, customer_id):
    if request.method == 'GET':
        form = CustomerEditForm(request)
        return render(request, 'customer_edit.html', {'form': form})
    obj = models.Customer.objects.filter(pk=customer_id).first()
    form = CustomerEditForm(request, data=request.POST, instance=obj)
    if not form.is_valid():
        return render(request, 'customer_edit.html', {'form': form})
    form.save()

    base_url = reverse('customer')
    param_url = request.GET.get('_filter')
    target = "{}?{}".format(base_url, param_url)

    return redirect(target)


def customer_reset(request, customer_id):
    if request.method == 'GET':
        form = CustomerPasswordForm()
        return render(request, 'customer_reset.html', {'form': form})
    obj = models.Customer.objects.filter(pk=customer_id, active=1).first()
    form = CustomerPasswordForm(data=request.POST, instance=obj)
    if not form.is_valid():
        return render(request, 'customer_reset.html', {'form': form})
    form.save()
    return redirect(reverse('customer'))


def customer_delete(request):
    if not request.method == 'GET':
        pass
    baseresopnse = BaseResponse()
    customer_id = request.GET.get('customer_id')
    if not customer_id:
        baseresopnse.detail = '请选择要删除的数据'
        return JsonResponse(baseresopnse.dict)
    exist = models.Customer.objects.filter(id=customer_id).exists()
    if not exist:
        baseresopnse.detail = '要删除的数据不存在'
        return JsonResponse(baseresopnse.dict)
    baseresopnse.status = True
    models.Customer.objects.filter(id=customer_id).update(active=0)
    return JsonResponse(baseresopnse.dict)


def customer_trade(request, customer_id):
    form = CustomerTradeModel()

    keyword = request.GET.get("keyword", "").strip()
    con = Q()
    if keyword:
        con.connector = 'OR'
        con.children.append(('memo__contains', keyword))
        con.children.append(('charge_type__contains', keyword))

    querylist = models.TransactionRecord.objects.filter(con).filter(customer_id=customer_id, customer_id__active=1,
                                                                    active=1).order_by('-id')
    pagination_object = Pagination(request, querylist)
    content = {'querylist': querylist[pagination_object.start: pagination_object.end],
               'paramstring': pagination_object.get_paramstring(),
               'form': form,
               'customer_id': customer_id, }
    return render(request, 'customer_trade.html', content)


def customer_trade_add(request, customer_id):
    if not request.method == 'POST':
        pass
    res = BaseResponse()
    form = CustomerTradeModel(data=request.POST)
    if not form.is_valid():
        res.detail = form.errors
        res.status = False
        return JsonResponse(res.dict)

    with transaction.atomic():
        customer_object = models.Customer.objects.filter(id=customer_id).select_for_update().first()
        # 通过基础的数据检验之后进行数据合法性校验
        charge_type = form.cleaned_data['charge_type']
        amount = form.cleaned_data['amount']
        # 包括扣款不能为负数，扣款数量不能超过账户余额
        if charge_type == 2 and amount > customer_object.balance:
            res.detail = {'amount': ["账户余额不足"]}
            res.status = False
            return JsonResponse(res.dict)
        elif charge_type == 2 and amount <= customer_object.balance:
            customer_object.balance -= amount
        else:
            customer_object.balance += amount
        customer_object.save()
        # 在数据库进行操作之后同步渲染到页面生成交易记录
        form.instance.creator_id = request.user_object.user_id
        form.instance.customer_id = customer_id
        form.save()

    res.status = True
    return JsonResponse(res.dict)

