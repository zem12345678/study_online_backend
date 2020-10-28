from mongoengine import Document
from mongoengine import fields


class BookInfo(Document):
    """
    定义图书文档类
    """
    btitle = fields.StringField(max_length=20, verbose_name='名称')
    bpub_date = fields.DateTimeField(verbose_name='发布日期')
    bread = fields.IntField(default=0, verbose_name='阅读量')
    bcomment = fields.IntField(default=0, verbose_name='评论量')
    is_delete = fields.BooleanField(default=False, verbose_name='逻辑删除')
    # MongoEngine的meta信息以meta属性指定
    meta = {
        'db_alias': 'test',    # 指定数据库别名
        'collection': 'tb_books',    # 指定集合名称
    }

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.btitle


class HeroInfo(Document):
    """
    定义英雄文档类
    """
    GENDER_CHOICES = (
        (0, 'female'),
        (1, 'male')
    )
    hname = fields.StringField(max_length=20, verbose_name='名称')
    hgender = fields.IntField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    hcomment = fields.StringField(max_length=200, null=True, verbose_name='描述信息')
    hbook = fields.ReferenceField(BookInfo, verbose_name='图书')  # 引用字段
    is_delete = fields.BooleanField(default=False, verbose_name='逻辑删除')

    meta = {
        'db_alias': 'test',
        'collection': 'tb_heros',
    }

    def __str__(self):
        return self.hname


class TestGridFS(Document):
    template = fields.FileField()

    meta = {
        'db_alias': 'test',
        'collection': 'test_gridfs',
    }
