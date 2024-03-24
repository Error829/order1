from django import forms
from django.core.exceptions import ValidationError

from web import models

from utils.bootstrapclass import Bootstrap


class OrderAddModel(Bootstrap, forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['url', 'count']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1.计算每条单价并且显示根据价格策略
        # 2.链接pricepolicy表
        info_list = []
        help_text_list = []
        price_list = models.PricePolicy.objects.all().order_by('amount')
        for item in price_list:
            uni_price = item.price / item.amount
            info_list.append([item.amount, uni_price])
            help_text_list.append("(>={}/¥{:.3f})".format(item.amount, uni_price))

        if help_text_list:
            self.fields['count'].help_text = "||".join(help_text_list)
        else:
            self.fields['count'].help_text = "请联系管理员设置价格"

        self.info_list = info_list
        self.price = None
        self.real_price = None
        self.user_id = request.user_object.user_id

    def clean_count(self):
        count = self.cleaned_data['count']
        if not self.info_list:
            raise ValidationError("请联系管理员设置价格")
        mini_value = self.info_list[0][0]
        # 1.数量不能低于最低价格策略数量
        uni_price = 0
        for i in range(len(self.info_list) - 1, -1, -1):
            amount, uni_price = self.info_list[i]
            if not count >= amount:
                continue
            break
        # 2.根据定位位置获取单价计算最终价格，确保最后价格低于用户余额
        if count < mini_value:
            raise ValidationError("最小额度为{}".format(mini_value))
        customer_object = models.Customer.objects.filter(id=self.user_id).first()
        user_balance = customer_object.balance
        user_percent = customer_object.level.percent
        real_price = count * uni_price * user_percent / 100
        if user_balance < real_price:
            raise ValidationError("账户余额不足")
        self.price = count * uni_price
        self.real_price = real_price
        return count
