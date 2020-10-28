from mongoengine import Document
from mongoengine.fields import StringField, DateTimeField, ListField, ReferenceField


class MediaFileProcess_m3u8(Document):
    # 错误信息
    errormsg = StringField()
    # ts列表
    tslist = ListField()


class MediaFile(Document):
    # 文件id
    fileId = StringField()
    # 文件名称
    fileName = StringField()
    # 文件原始名称
    fileOriginalName = StringField()
    # 文件路径
    filePath = StringField()
    # 文件url
    fileUrl = StringField()
    # 文件类型
    fileType = StringField()
    # mimetype
    mimeType = StringField()
    # 文件大小
    fileSize = StringField()
    # 文件状态
    fileStatus = StringField()
    # 上传时间
    uploadTime = DateTimeField()
    # 处理状态
    processStatus = StringField()
    # tag标签用于查询
    tag = StringField()
    # hls处理
    mediaFileProcess_m3u8 = ReferenceField(MediaFileProcess_m3u8)

    # 根据file_id获取MediaFile
    @classmethod
    def find_by_id(cls, file_id):
        return cls.objects.filter(fileId=file_id).first()
