# Generated by Django 3.2 on 2024-03-08 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrator',
            name='active',
            field=models.SmallIntegerField(choices=[(1, '激活'), (0, '删除')], default=1, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='customer',
            name='active',
            field=models.SmallIntegerField(choices=[(1, '激活'), (0, '删除')], default=1, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='level',
            name='active',
            field=models.SmallIntegerField(choices=[(1, '激活'), (0, '删除')], default=1, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='order',
            name='active',
            field=models.SmallIntegerField(choices=[(1, '激活'), (0, '删除')], default=1, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='transactionrecord',
            name='active',
            field=models.SmallIntegerField(choices=[(1, '激活'), (0, '删除')], default=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(2, '正在执行'), (4, '失败'), (5, '无'), (3, '完成'), (1, '待执行')], default=5, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='charge_type',
            field=models.IntegerField(choices=[(5, '撤单'), (3, '创建订单'), (1, '充值'), (4, '删除订单'), (2, '扣款')], verbose_name='交易类型'),
        ),
    ]
