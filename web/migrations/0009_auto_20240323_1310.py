# Generated by Django 3.2 on 2024-03-23 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20240322_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(5, '已撤单'), (4, '失败'), (3, '完成'), (2, '正在执行'), (1, '待执行')], default=5, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='charge_type',
            field=models.IntegerField(choices=[(5, '撤单'), (3, '创建订单'), (1, '充值'), (2, '扣款'), (4, '删除订单')], verbose_name='交易类型'),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='order_oid',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='订单号'),
        ),
    ]
