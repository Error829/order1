from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin


class UserInfo(object):
    def __init__(self, user_id, role, username, password):
        self.user_id = user_id
        self.role = role
        self.username = username
        self.password = password
        self.menu_name = None
        self.path_list = []
        # self.parent_path = None


class LoginSessionsCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 用户不需登录就可以访问的网址
        if request.path_info in settings.ORDER_WHITE_URL:
            return
        # 未成功获取到用户对象返回登录页面
        data_dict = request.session.get(settings.ORDER_USER_INFO)
        if not data_dict:
            return redirect(settings.ORDER_LOGIN_URL)
        # 成功获取到用户session中的user_info信息了,进行封装成对象
        user_object = UserInfo(**data_dict)
        request.user_object = user_object
        #

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # 1.获取所有公共权限
        public_permissions = settings.ORDER_PREMISSION_PUBLIC
        url_now = request.resolver_match.url_name
        print(url_now)
        # 2.检查是否在公共权限中，如果是就继续（白名单）
        if url_now in public_permissions:
            return None
        # 3.根据用户登录角色获取其角色权限
        role_now = request.user_object.role
        permissions = settings.ORDER_PREMISSION[role_now]
        # 4.检查其角色权限和其访问的url是否一致（包含）
        if url_now not in permissions:
            # 5.权限不包含则返回权限不足模板
            if request.is_ajax():
                return JsonResponse({'status': False, 'detail': '无权访问'})
            else:
                return render(request, 'error.html')
        # 6.权限校验通过则继续
        # 7.根据权限配置文件中的parent属性向上获取文件路径导航并存储
        menu_now = permissions[url_now]['title']
        path_list = [menu_now]
        # request.user_object.parent_path = permissions[url_now]['parent']
        while permissions[url_now]['parent']:
            url_now = permissions[url_now]['parent']
            menu_now = permissions[url_now]['title']
            path_list.append(menu_now)
        path_list.append('首页')
        path_list.reverse()
        # 8.将menu_name和文件路径信息存入request对象中
        request.user_object.path_list = path_list
        request.user_object.menu_name = url_now
        return None

    def process_response(self, request, response):
        return response
