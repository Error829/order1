from django import template
from django.urls import reverse
from django.conf import settings
from django.http import QueryDict

from django.utils.safestring import mark_safe

register = template.Library()


def has_permission(request, button_name):
    # 1.获取用户角色，获取按钮name
    role = request.user_object.role
    permission = button_name
    # 2.获取所有公共权限
    public_permission = settings.ORDER_PREMISSION_PUBLIC
    # 3.根据用户角色读取配置文件获取所有权限
    permission_dict = settings.ORDER_PREMISSION[role]
    # 4.比对name是否在公共/角色权限中 若全不存在则返回空字符串
    if permission not in public_permission and permission not in permission_dict:
        return False
    return True


@register.simple_tag
def add_button(request, button_name):
    if not has_permission(request, button_name):
        return ""
    # 5.name在权限列表中 则返回定制按钮即可

    url = reverse(button_name)
    tpl = "<button class=\"btn btn-success\"><a href=\"{}\" style=\"text-decoration: none\"><b style=\"color: black\">添加</b></a></button>".format(
        url)
    return mark_safe(tpl)


@register.simple_tag
def edit_button(request, button_name, *args, **kwargs):
    if not has_permission(request, button_name):
        return ""
    # 5.name在权限列表中 则返回定制按钮即可

    param = request.GET.urlencode()
    new_querydict = QueryDict(mutable=True)
    new_querydict['_filter'] = param
    filter_string = new_querydict.urlencode()

    url = reverse(button_name, args=args, kwargs=kwargs)
    tpl = "<button class=\"btn btn-secondary\"><a href=\"{}?{}\"style=\"text-decoration: none\"><b style=\"color: black\">编辑</b></a></button>".format(
        url, filter_string)
    return mark_safe(tpl)


@register.simple_tag
def delete_button(request, button_name, target):
    if not has_permission(request, button_name):
        return ""
    # 5.name在权限列表中 则返回定制按钮即可
    _id = target
    tpl = "<button class=\"btn btn-danger btn-delete\" value=\"{}\" style=\"color: black\"data-bs-toggle=\"modal\" data-bs-target=\"#deleteModal\">删除</button>".format(
        _id)
    return mark_safe(tpl)
