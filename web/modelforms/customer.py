from django import forms
from django.core.exceptions import ValidationError

from web import models
from utils.encrypt import md5
from utils.bootstrapclass import Bootstrap


class CustomerForm(Bootstrap, forms.ModelForm):
    repeat_password = forms.CharField(label='重复密码', widget=forms.PasswordInput())

    class Meta:
        model = models.Customer
        fields = ['username', 'mobile', 'password', 'repeat_password', 'level']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['level'].queryset = models.Level.objects.filter(active=1)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = md5(password)
        return password

    def clean_repeat_password(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        repeat_password = md5(repeat_password)
        if password != repeat_password:
            raise ValidationError('两次输入密码不一致')
        return repeat_password


class CustomerEditForm(Bootstrap, forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['username', 'mobile', 'level']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['level'].queryset = models.Level.objects.filter(active=1)


class CustomerPasswordForm(Bootstrap, forms.ModelForm):
    repeat_password = forms.CharField(label='重复密码', widget=forms.PasswordInput())

    class Meta:
        model = models.Customer
        fields = ['password', 'repeat_password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = md5(password)
        return password

    def clean_repeat_password(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        repeat_password = md5(repeat_password)
        if password != repeat_password:
            raise ValidationError('两次输入密码不一致')
        return repeat_password


class CustomerTradeModel(Bootstrap, forms.ModelForm):
    class Meta:
        model = models.TransactionRecord
        fields = ['charge_type', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['charge_type'].choices = [(1, '充值'), (2, '扣款')]
