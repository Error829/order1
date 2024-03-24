from web import models
from django import forms
from django.urls import reverse
from django.shortcuts import render, redirect

from web.modelforms.level import LevelModelForm


def level(request):
    querylist = models.Level.objects.filter(active=1)
    return render(request, 'level.html', {'querylist': querylist})


def level_add(request):
    # 用modelform创建相应模板
    # 在页面上渲染相应字段
    if request.method == 'GET':
        form = LevelModelForm()
        return render(request, 'level_add.html', {'form': form})
    # 提交进行is_valid()查验
    form = LevelModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'level_add.html', {'form': form})
    # 数据合法则写入数据库并返回level页面 redirect
    form.save()
    return redirect(reverse('level'))


def level_edit(request, level_id):
    # 用modelform创建相应模板
    # 在页面上渲染相应字段
    if request.method == 'GET':
        form = LevelModelForm()
        return render(request, 'level_edit.html', {'form': form})
    # # 提交进行is_valid()查验
    level_object = models.Level.objects.get(id=level_id)
    form = LevelModelForm(data=request.POST, instance=level_object)
    if not form.is_valid():
        return render(request, 'level_edit.html', {'form': form})
    # 数据合法则写入数据库并返回level页面 redirect
    form.save()
    return redirect(reverse('level'))


def level_delete(request, level_id):
    stauts = models.Customer.objects.filter(level_id=level_id, active=1).exists()
    if not stauts:
        return render(request, 'error_delete.html')
    models.Level.objects.filter(id=level_id).update(active=0)
    return redirect(reverse('level'))

# def level_return(request, level_id):
#     print(reverse(request.user_object.parent_path))
#     return redirect(reverse(request.user_object.parent_path))
