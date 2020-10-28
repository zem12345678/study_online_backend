from rest_framework.views import APIView
from utils.fdfs.client import FdfsClient
from filesystem.models import FileSystem
from rest_framework.response import Response
from common.exceptions import cast_exception
from common import response_code


class FileSystemView(APIView):

    def post(self, request, *args, **kwargs):
        # 实例化Fdfs客户端类
        client = FdfsClient()
        file_id = ''
        for i in request.FILES:
            # 读取文件buffer
            if hasattr(request.FILES[i].file, 'getbuffer'):
                buffer = request.FILES[i].file.getbuffer()
            elif hasattr(request.FILES[i].file, 'read'):
                buffer = request.FILES[i].file.read()
            else:
                buffer = b''
                cast_exception(response_code.COURSE_PIC_UPLOAD_ERROR)
            # 将buffer上传到FastDFS
            try:
                resp = client.upload_buffer(buffer, request.FILES[i].content_type.split('/')[-1])
                file_id = resp.get('file_id')
            except Exception as e:
                cast_exception(response_code.COURSE_PIC_UPLOAD_ERROR)
            # 将文件信息保存到FileSystem
            filesystem = FileSystem(filePath=file_id, fileSize=str(request.FILES[i].size), fileName=request.FILES[i].name,
                       fileType=request.FILES[i].content_type, filetag=request.data.get('filetag'))
            filesystem.save()
            # 将Fileid返回前端
            return Response({'fileId': file_id})
