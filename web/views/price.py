from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from web import models
from utils.pagination import Pagination
from utils.BaseResponse import BaseResponse
from web.modelforms.price import PriceForm


def price(request):
    querylist = models.PricePolicy.objects.all()
    pagination_object = Pagination(request, querylist)
    print(pagination_object.start, pagination_object.end)
    content = {'querylist': querylist[pagination_object.start: pagination_object.end],
               'paramstring': pagination_object.get_paramstring()}
    return render(request, 'price.html', content)


def policy_delete(request):
    if not request.method == 'GET':
        pass
    baseresopnse = BaseResponse()
    policy_id = request.GET.get('policy_id')
    if not policy_id:
        baseresopnse.detail = '请选择要删除的数据'
        return JsonResponse(baseresopnse.dict)
    exist = models.PricePolicy.objects.filter(id=policy_id).exists()
    if not exist:
        baseresopnse.detail = '要删除的数据不存在'
        return JsonResponse(baseresopnse.dict)
    baseresopnse.status = True
    models.PricePolicy.objects.filter(id=policy_id).delete()
    return JsonResponse(baseresopnse.dict)


def price_edit(request, policy_id):
    if request.method == 'GET':
        form = PriceForm()
        return render(request, 'price_edit.html', {'form': form})
    policy_object = models.PricePolicy.objects.filter(id=policy_id).first()
    form = PriceForm(data=request.POST, instance=policy_object)
    if not form.is_valid():
        return render(request, 'price_edit.html', {'form': form})
    form.save()
    return redirect(reverse('price'))


def price_add(request):
    if request.method == 'GET':
        form = PriceForm()
        return render(request, 'price_add.html', {'form': form})
    form = PriceForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'price_add.html', {'form': form})
    form.save()
    return redirect(reverse('price'))
