import os
import sys

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from utils.encrypt import md5

BASEPATH = os.path.dirname(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(BASEPATH)


class LoginForm(forms.Form):
    role = forms.ChoiceField(
        label="权限",
        required=True,
        choices=(('1', "用户"), ('2', "管理员")),
        widget=forms.Select(attrs={'class': "form-control"})
    )
    username = forms.CharField(
        label="用户名",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"})
    )
    password = forms.CharField(
        label="密码",
        required=True,
        min_length=4,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        illegal_list = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '=', '+', '[', ']', '{',
                        '}', '\\', '|']
        for char in username:
            if char not in illegal_list:
                continue
            raise ValidationError("用户名含有非法字符")
        return username

    def clean_password(self):
        flag = False
        password = self.cleaned_data['password']
        print(password, password.isdecimal())
        if password.isdecimal():
            flag = True
        if flag:
            raise ValidationError("密码必须含有字母")
        return md5(password)


class SmsLoginForm(forms.Form):
    role = forms.ChoiceField(
        label="权限",
        required=True,
        choices=(('1', "用户"), ('2', "管理员")),
        widget=forms.Select(attrs={'class': "form-control"})
    )
    mobile = forms.CharField(
        label="手机号",
        required=True,
        validators=[RegexValidator('^1[3|4|5|7|8][0-9]{9}$', '手机格式错误')],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "手机号"})
    )
    code = forms.CharField(
        label="短信验证码",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "验证码"})
    )


class MobileForm(forms.Form):
    role = forms.ChoiceField(
        label="权限",
        required=True,
        choices=(('1', "用户"), ('2', "管理员")),
    )
    mobile = forms.CharField(
        label="手机号",
        required=True,
        validators=[RegexValidator('^1[3|4|5|7|8][0-9]{9}$', '手机格式错误')],
    )
