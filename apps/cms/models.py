from datetime import datetime

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, ReferenceField, DateTimeField, ListField, EmbeddedDocumentField, FileField, \
    DictField


class CmsSite(Document):
    """
    Cms站点，一个站点包括多个页面
    """
    # 站点名称
    siteName = StringField(required=True)
    # 站点域名
    siteDomain = StringField(required=True)
    # 站点端口
    sitePort = StringField(required=True)
    # 站点访问地址
    siteWebPath = StringField(required=True)
    # 创建时间
    siteCreateTime = DateTimeField(default=datetime.now)
    # 站点在服务器中存储的物理路径，绝对路径
    sitePhysicalPath = StringField(required=True)


class CmsTemplate(Document):
    """
    Cms模板，多个页面可以使用相同的模板
    """
    # 站点ID
    siteId = ReferenceField(CmsSite, required=True)
    # 模版名称
    templateName = StringField(required=True)
    # 模版参数
    templateParameter = StringField()
    # 模版文件Id
    templateFileId = FileField()


class CmsPage(Document):
    """
    Cms页面信息
    """
    # 站点 *
    siteId = ReferenceField(CmsSite, required=True)
    # 页面名称 *
    pageName = StringField(required=True)
    # 页面别名
    pageAlias = StringField(default='', null=True)
    # 访问地址 *
    pageWebPath = StringField(required=True)
    # 页面保存在站点的物理路径，是站点物理路径的子路径 *
    pagePhysicalPath = StringField(required=True)
    # 类型（静态/动态）*
    pageType = StringField(default='0')
    # 页面模版
    pageTemplate = StringField()
    # 页面静态化内容
    pageHtml = StringField()
    # 状态
    pageStatus = StringField(null=True)
    # 创建时间
    pageCreateTime = DateTimeField(default=datetime.now)
    # 模版id *
    templateId = ReferenceField(CmsTemplate, required=True)
    # 页面参数列表，暂未使用
    pageParams = ListField()
    # 静态文件Id
    htmlFileId = FileField(null=True)
    # 数据Url
    dataUrl = StringField(null=True)

    @classmethod
    def find_by_id(cls, page_id):
        return cls.objects(id=page_id).first()


class CmsConfigModel(EmbeddedDocument):
    """
    CMS配置的数据模型
    """
    # 主键
    key = StringField()
    # 项目名称
    name = StringField()
    # 项目url
    url = StringField()
    # 项目简单值
    value = StringField()
    # 项目复杂值
    mapValue = DictField()


class CmsConfig(Document):
    """
    CMS配置
    """
    # 数据模型的名称
    name = StringField()
    # 数据模型项目
    model = ListField(EmbeddedDocumentField(CmsConfigModel))


class SysDictionaryValue(EmbeddedDocument):
    """
    系统配置字典值
    """
    sd_id = StringField()
    sd_name = StringField()
    sd_status = StringField()


class SysDictionary(Document):
    """
    系统配置字典
    """
    d_name = StringField()
    d_type = StringField()
    d_value = ListField(EmbeddedDocumentField(SysDictionaryValue))
