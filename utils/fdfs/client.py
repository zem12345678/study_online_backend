import os.path
from cz_study.settings import BASE_DIR
from fdfs_client.client import Fdfs_client


class FdfsClient:
    client = None

    def __init__(self):
        if self.client is None:
            self.client = Fdfs_client(os.path.join(BASE_DIR, 'utils/fdfs/client.conf'))

    # 上传文件buffer
    def upload_buffer(self, buffer, ext_name=None):
        result = self.client.upload_appender_by_buffer(buffer, ext_name)
        return {'file_id': result.get('Remote file_id').decode()}
