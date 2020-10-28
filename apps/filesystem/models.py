from rest_framework_mongoengine.fields import Document
from mongoengine.fields import StringField


class FileSystem(Document):
    # 文件请求路径
    filePath = StringField()
    # 文件大小
    fileSize = StringField()
    # 文件名称
    fileName = StringField()
    # 文件类型
    fileType = StringField()
    # 图片宽度
    fileWidth = StringField()
    # 图片高度
    fileHeight = StringField()
    # 用户id，用于授权
    userId = StringField()
    # 业务key
    businesskey = StringField()
    # 业务标签
    filetag = StringField()
    # 文件元信息
    metadata = StringField()
