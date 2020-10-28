import os
from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from utils import xmd5
from media.models import MediaFile
from media.serializers import MediaFileSerializer
from common.exceptions import cast_exception
from common import response_code, sys_dict
from cz_study import settings
from celery_tasks.media.tasks import media_process
from common.paginations import PathPagePagination


class MediaUploadViewSet(ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer

    # 获取相对文件夹路径
    def get_file_relative_folder_path(self, file_md5):
        return file_md5[0:1] + '/' + file_md5[1:2] + '/' + file_md5 + '/'

    # 获取文件夹路径
    def get_file_folder_path(self, file_md5):
        return settings.COURSE_PUBLISH['media_upload_location'] + self.get_file_relative_folder_path(file_md5)

    # 获取文件路径
    def get_file_path(self, file_md5, file_ext):
        return self.get_file_folder_path(file_md5) + file_md5 + '.' + file_ext

    def _register(self, file_md5, file_name, file_size, mimetype, file_ext):
        file_folder_path = self.get_file_folder_path(file_md5)
        file_path = self.get_file_path(file_md5, file_ext)
        # 检查文件是否已经存在
        exists = os.path.exists(file_path)
        media_file = MediaFile.find_by_id(file_md5)
        if exists and media_file:
            cast_exception(response_code.UPLOAD_FILE_REGISTER_EXIST)
        # 创建相关目录
        try:
            os.makedirs(file_folder_path)
        except Exception as e:
            print(e)

    # 上传注册
    def register(self, request, *args, **kwargs):
        self._register(request.data['fileMd5'], request.data['fileName'], request.data['fileSize'],
                       request.data['mimetype'], request.data['fileExt'])
        return Response()

    # 获取分块文件夹路径
    def get_chunk_file_folder_path(self, file_md5):
        return self.get_file_folder_path(file_md5) + 'chunk/'

    def _check_chunk(self, file_md5, chunk, chunk_size):
        chunk_file_folder_path = self.get_chunk_file_folder_path(file_md5)
        exists = os.path.exists(chunk_file_folder_path + chunk)
        return exists

    # 分块检查
    def checkchunk(self, request, *args, **kwargs):
        exists = self._check_chunk(request.data['fileMd5'], request.data['chunk'], request.data['chunkSize'])
        return Response({'exists': exists})

    def _upload_chunk(self, file, file_md5, chunk):
        chunk_file_folder_path = self.get_chunk_file_folder_path(file_md5)
        chunk_file_path = chunk_file_folder_path + chunk
        try:
            os.makedirs(chunk_file_folder_path)
        except Exception as e:
            print(e)
        with open(chunk_file_path, 'wb+') as output_file:
            output_file.write(file.read())

    # 上传分块
    def uploadchunk(self, request, *args, **kwargs):
        self._upload_chunk(request.data['file'], request.data['fileMd5'], request.data['chunk'])
        return Response()

    def _merge_chunk(self, file_md5, file_name, file_size, mimetype, file_ext):
        chunk_file_folder_path = self.get_chunk_file_folder_path(file_md5)
        _, _, files = next(os.walk(chunk_file_folder_path))
        files.sort(key=lambda name: int(name))
        # 将分块文件写入目标文件
        file_path = self.get_file_path(file_md5, file_ext)
        merge_file = open(file_path, 'wb+')
        for file_name in files:
            with open(chunk_file_folder_path+file_name, 'rb') as chunk_file:
                merge_file.write(chunk_file.read())
        if file_md5 != xmd5.get_file_md5(merge_file):
            cast_exception(response_code.UPLOAD_FILE_REGISTER_FAIL)
        merge_file.close()
        # 保存文件信息
        media_file = MediaFile(fileId=file_md5, fileOriginalName=file_name, fileName=file_md5 + '.' + file_ext,
                               filePath=self.get_file_relative_folder_path(file_md5),
                               fileSize=file_size, uploadTime=datetime.now(), mimeType=mimetype, fileType=file_ext,
                               fileStatus=sys_dict.MEDIA_FILE_STATUS_UPLOAD)
        media_file.save()
        media_process.delay(file_md5)
        return media_file

    # 合并分块
    def mergechunk(self, request, *args, **kwargs):
        self._merge_chunk(request.data['fileMd5'], request.data['fileName'], request.data['fileSize'],
                          request.data['mimetype'], request.data['fileExt'])
        return Response()


class MediaFileViewSet(ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    pagination_class = PathPagePagination

    def get_queryset(self):
        filters = {}
        tag = self.request.query_params.get('tag')
        if tag:
            filters.update({'tag': tag})
        process_status = self.request.query_params.get('processStatus')
        if process_status:
            filters.update({'processStatus': process_status})
        file_name = self.request.query_params.get('fileOriginalName')
        if file_name:
            filters.update({'fileOriginalName__contains': file_name})
        queryset = super().get_queryset()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset
