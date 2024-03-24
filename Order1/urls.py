"""Order1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path
from web.views import login, customer, level, price, order

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("login/", login.login, name="login"),
    path("sms_login/", login.sms_login, name="sms_login"),
    path("sms_send/", login.sms_send, name="sms_send"),
    path("home/", login.home, name="home"),
    path('logout/', login.logout, name="logout"),

    path('level/', level.level, name="level"),
    path('level/add/', level.level_add, name="level_add"),
    path('level/edit/<int:level_id>/', level.level_edit, name="level_edit"),
    path('level/delete/<int:level_id>/', level.level_delete, name="level_delete"),

    path('customer/', customer.customer, name="customer"),
    path('customer/add/', customer.customer_add, name="customer_add"),
    path('customer/edit/<int:customer_id>/', customer.customer_edit, name="customer_edit"),
    path('customer/reset/<int:customer_id>/', customer.customer_reset, name="customer_reset"),
    path('customer/delete/', customer.customer_delete, name="customer_delete"),
    path('customer/trade/<int:customer_id>/', customer.customer_trade, name="customer_trade"),
    path('customer/trade/<int:customer_id>/add/', customer.customer_trade_add, name="customer_trade_add"),

    path('price/', price.price, name="price"),
    path('price/delete/', price.policy_delete, name="policy_delete"),
    path('price/edit/<int:policy_id>/', price.price_edit, name="price_edit"),
    path('price/add/', price.price_add, name="price_add"),

    path('order/', order.order, name="order"),
    path('order/add/', order.order_add, name="order_add"),
    path('order/list/', order.order_list, name="order_list"),
    path('order/cancel/', order.order_cancel, name="order_cancel"),
]
