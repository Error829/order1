from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class ActiveBaseModel(models.Model):
    class Meta:
        abstract = True

    active = models.SmallIntegerField(verbose_name="状态", default=1, choices=((1, "激活"), (0, "删除")))


class Administrator(ActiveBaseModel):
    """ 管理员表 """
    username = models.CharField(verbose_name="用户名", max_length=32, db_index=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    mobile = models.CharField(verbose_name="手机号", max_length=11, db_index=True)
    create_date = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)


class Level(ActiveBaseModel):
    """ 级别表 """
    title = models.CharField(verbose_name="级别", max_length=32)
    percent = models.IntegerField(verbose_name="折扣", help_text='输入0-100整数为折扣百分比')

    def __str__(self):
        return self.title


class Customer(ActiveBaseModel):
    """ 客户表 """
    username = models.CharField(verbose_name="用户名", max_length=32, db_index=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    mobile = models.CharField(verbose_name="手机号", max_length=11, db_index=True,
                              validators=[RegexValidator('^1[3|4|5|7|8][0-9]{9}$', '手机格式错误')], )
    balance = models.DecimalField(verbose_name="账户余额", default=0, max_digits=10, decimal_places=2)
    level = models.ForeignKey(verbose_name="级别", to="Level", on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
    creator = models.ForeignKey(verbose_name="创建者", to="Administrator", on_delete=models.CASCADE)


class PricePolicy(models.Model):
    """价格策略表"""
    amount = models.IntegerField(verbose_name="数量", default=0)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)


class Order(ActiveBaseModel):
    status_choices = {
        (1, "待执行"),
        (2, "正在执行"),
        (3, "完成"),
        (4, "失败"),
        (5, "已撤单")
    }
    status = models.IntegerField(verbose_name="状态", choices=status_choices, default=5)

    oid = models.CharField(verbose_name="订单号", max_length=64, unique=True)
    url = models.CharField(verbose_name="视频地址", max_length=64, db_index=True)
    count = models.IntegerField(verbose_name="数量", default=0)

    price = models.DecimalField(verbose_name="原价", max_digits=10, decimal_places=2)
    real_price = models.DecimalField(verbose_name="折扣价", max_digits=10, decimal_places=2)

    old_view_count = models.CharField(verbose_name="视频原播放量", max_length=64)

    create_date = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
    customer = models.ForeignKey(verbose_name="下单用户", to=Customer, on_delete=models.CASCADE)
    memo = models.TextField(verbose_name="备注", blank=True)


class TransactionRecord(ActiveBaseModel):
    """交易记录表"""
    charge_type_class_mapping = {
        1: "success",
        2: "danger",
        3: "default",
        4: "info",
        5: "primary",
    }
    charge_type_choices = {
        (1, "充值"),
        (2, "扣款"),
        (3, "创建订单"),
        (4, "删除订单"),
        (5, "撤单"),
    }
    charge_type = models.IntegerField(verbose_name="交易类型", choices=charge_type_choices)

    customer = models.ForeignKey(verbose_name="客户", to='Customer', on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="金额", max_digits=10, decimal_places=2, default=0)

    creator = models.ForeignKey(verbose_name="管理员", to='Administrator', on_delete=models.CASCADE, blank=True, null=True)

    order_oid = models.CharField(verbose_name="订单号", max_length=64, blank=True, null=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    memo = models.TextField(verbose_name="备注", blank=True)
