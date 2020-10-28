import json
from datetime import datetime
from django.db import models
from ucenter.models import CzUser
from common import sys_dict


class CzOrders(models.Model):
    """
    订单主表：记录订单的主要信息
    """
    order_number = models.CharField(verbose_name='订单号', max_length=32, primary_key=True)
    initial_price = models.FloatField(verbose_name='定价', null=True)
    price = models.FloatField(verbose_name='交易价', null=True)
    start_time = models.DateTimeField(verbose_name='支付起始时间', null=True)
    end_time = models.DateTimeField(verbose_name='支付过期时间', null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    status = models.CharField(verbose_name='交易状态', max_length=32, null=True)
    user_id = models.ForeignKey(CzUser, verbose_name='用户id', null=True, db_column='user_id', related_name='purchaser')
    details = models.CharField(verbose_name='订单明细', max_length=1000, null=True)

    class Meta:
        db_table = 'cz_orders'


class CzOrdersDetail(models.Model):
    """
    订单明细表：记录订单的明细信息
    """
    order_number = models.ForeignKey(CzOrders, on_delete=models.DO_NOTHING)
    item_id = models.IntegerField(verbose_name='商品id', unique=True)
    item_num = models.IntegerField(verbose_name='商品数量')
    item_price = models.FloatField(verbose_name='金额')
    valid = models.CharField(verbose_name='课程有效性', max_length=32)
    start_time = models.DateTimeField(verbose_name='课程开始时间', null=True)
    end_time = models.DateTimeField(verbose_name='课程结束时间', null=True)

    class Meta:
        db_table = 'cz_orders_detail'


class CzOrdersPay(models.Model):
    """
    订单支付表：记录订单的支付状态
    """
    order_number = models.ForeignKey(CzOrders, db_column='order_number', verbose_name='订单号', max_length=32)
    pay_number = models.CharField(verbose_name='支付系统订单号', unique=True, max_length=32, null=True)
    status = models.CharField(verbose_name='交易状态', max_length=32)
    pay_time = models.DateTimeField(verbose_name='支付时间', null=True)
    pay_through = models.CharField(verbose_name='支付方式', null=True, max_length=10)

    class Meta:
        db_table = 'cz_orders_pay'


class CzTask(models.Model):
    """
    待处理任务表：在任务表中包括了交换机的名称、路由key等信息为了是将任务的处理做成一个通用的功能。考虑分布式系统并发读取任务处理任务的情况发生项目使用乐观锁的方式解决并发问题。
    """
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', null=True)
    task_type = models.CharField(verbose_name='任务类型', max_length=32, null=True)
    mq_exchange = models.CharField(verbose_name='交换机名称', max_length=64, null=True)
    mq_routingkey = models.CharField(verbose_name='routing key', max_length=64, null=True)
    request_body = models.CharField(verbose_name='任务请求的内容', max_length=512, null=True)
    version = models.IntegerField(verbose_name='乐观锁版本号', null=True)
    status = models.CharField(verbose_name='任务状态', max_length=32, null=True)
    errormsg = models.CharField(verbose_name='任务错误信息', max_length=512, null=True)

    class Meta:
        db_table = 'cz_task'


class CzTaskHis(models.Model):
    """
    已完成任务表
    """
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', null=True)
    task_type = models.CharField(verbose_name='任务类型', max_length=32, null=True)
    mq_exchange = models.CharField(verbose_name='交换机名称', max_length=64, null=True)
    mq_routingkey = models.CharField(verbose_name='routing key', max_length=64, null=True)
    request_body = models.CharField(verbose_name='任务请求的内容', max_length=512, null=True)
    version = models.IntegerField(verbose_name='乐观锁版本号', null=True)
    status = models.CharField(verbose_name='任务状态', max_length=32, null=True)
    errormsg = models.CharField(verbose_name='任务错误信息', max_length=512, null=True)

    class Meta:
        db_table = 'cz_task_his'
