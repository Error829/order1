from copy import deepcopy

from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('tag/menu.html')
def menu_create(request):
    role = request.user_object.role

    user_menu = deepcopy(settings.ORDER_MENU[role])
    for item in user_menu:
        for child in item['children']:
            if child['name'] == request.user_object.menu_name:
                child['class'] = 'active'

    return {'user_menu_list': user_menu}
