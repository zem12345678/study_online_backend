from common import sys_dict
from celery_tasks.main import app
from utils import video
from cz_study import settings
from media.models import MediaFile, MediaFileProcess_m3u8


@app.task(bind=True, name='media_process')
def media_process(self, media_id):
    server_path = settings.COURSE_PUBLISH['media_upload_location']
    # 使用media_id查询文件信息
    media_file = MediaFile.find_by_id(media_id)
    if media_file is None:
        return
    # 不是avi文件不需处理
    if media_file.fileType != 'avi':
        media_file.processStatus = sys_dict.VIDEO_PROCESS_STATUS_NONE
        media_file.save()
        return
    # 是avi文件则初始化状态
    else:
        media_file.processStatus = sys_dict.VIDEO_PROCESS_STATUS_PROCESSING
        media_file.save()
    # 使用工具类生成mp4文件
    video_path = server_path + media_file.filePath + media_file.fileName
    mp4_name = media_file.fileId + '.mp4'
    mp4_folder_path = server_path + media_file.filePath
    mp4_video_util = video.Mp4VideoUtil(video_path, mp4_name, mp4_folder_path)
    result = mp4_video_util.generate_mp4()
    if result is None or result != 'success':
        media_file.processStatus = sys_dict.VIDEO_PROCESS_STATUS_FAIL
        media_file_process_m3u8 = MediaFileProcess_m3u8(errormsg=result)
        media_file_process_m3u8.save()
        media_file.mediaFileProcess_m3u8 = media_file_process_m3u8
        media_file.save()
        return
    # 使用工具类生成m3u8文件
    mp4_video_path = server_path + media_file.filePath + mp4_name
    m3u8_name = media_file.fileId + '.m3u8'
    m3u8_folder_path = server_path + media_file.filePath + 'hls/'
    hls_video_util = video.HlsVideoUtil(mp4_video_path, m3u8_name, m3u8_folder_path)
    ts_result = hls_video_util.generate_m3u8()
    if ts_result is None or ts_result != 'success':
        media_file.processStatus = sys_dict.VIDEO_PROCESS_STATUS_FAIL
        media_file_process_m3u8 = MediaFileProcess_m3u8(errormsg=result)
        media_file_process_m3u8.save()
        media_file.mediaFileProcess_m3u8 = media_file_process_m3u8
        media_file.save()
        return
    ts_list = hls_video_util.get_ts_list()
    media_file.processStatus = sys_dict.VIDEO_PROCESS_STATUS_SUCCESS
    media_file_process_m3u8 = MediaFileProcess_m3u8(tslist=ts_list)
    media_file_process_m3u8.save()
    media_file.fileUrl = media_file.filePath + 'hls/' + m3u8_name
    media_file.save()
