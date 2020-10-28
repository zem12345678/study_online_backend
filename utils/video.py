import subprocess
import re
import os
import shutil
from cz_study import settings


# 视频处理基类
class VideoUtil:
    ffmpeg_path = settings.COURSE_PUBLISH['ffmpeg_path']

    def __init__(self, ffmpeg_path=None):
        if ffmpeg_path:
            self.ffmpeg_path = ffmpeg_path

    # 执行命令并获取命令执行结果
    @staticmethod
    def run_command_and_get_output(command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            process_result = process.stdout.read()
            return process_result.decode('utf-8', errors='ignore')
        except Exception as e:
            print(e)
            return ''

    # 获取视频文件时长
    def get_video_time(self, video_path):
        # Duration: 00:14:35.20, start: 0.000000, bitrate: 480 kb/s
        command_output = self.run_command_and_get_output(self.ffmpeg_path + ' -i ' + video_path)
        time_strings = re.findall('Duration: (\d+):(\d+):(\d+)\.(\d+)', command_output)
        if isinstance(time_strings, list) and len(time_strings) > 0:
            return time_strings[0]
        return None

    # 检查两个视频的时长是否相等(基本相等)
    def check_video_time(self, source, target, threshold=50):
        source_time = self.get_video_time(source)
        target_time = self.get_video_time(target)
        print(source_time, target_time)
        if source_time is None or target_time is None:
            return False
        if source_time == target_time:
            return True
        sh, sm, ss, sms = source_time
        th, tm, ts, tms = target_time
        if sh == th and sm == tm and abs(int(ss) * 1000 + int(sms) - int(ts) * 1000 - int(tms)) <= threshold:
            return True
        return False


# avi转mp4的工具类
class Mp4VideoUtil(VideoUtil):

    def __init__(self, video_path, mp4_name, mp4_folder_path, ffmpeg_path=None):
        super().__init__(ffmpeg_path)
        self.video_path = video_path
        self.mp4_name = mp4_name
        self.mp4_folder_path = mp4_folder_path

    # 清除旧文件
    @staticmethod
    def clear_mp4(mp4_file_path):
        if os.path.exists(mp4_file_path) and os.path.isfile(mp4_file_path):
            os.remove(mp4_file_path)

    # 生成mp4文件
    def generate_mp4(self):
        mp4_file_path = self.mp4_folder_path + self.mp4_name
        self.clear_mp4(mp4_file_path)
        command = self.ffmpeg_path + ' -i ' + self.video_path + ' -c:v libx264 -s 1280x720 -pix_fmt yuv420p -b:a 63k ' \
                                                                '-b:v 753k -r 18 ' + mp4_file_path
        command_output = self.run_command_and_get_output(command)
        time_equal = self.check_video_time(self.video_path, mp4_file_path)
        if not time_equal:
            return command_output
        else:
            return 'success'


# mp4转M3u8工具类
class HlsVideoUtil(VideoUtil):

    def __init__(self, video_path, m3u8_name, m3u8_folder_path, ffmpeg_path=None):
        super().__init__(ffmpeg_path)
        self.video_path = video_path
        self.m3u8_name = m3u8_name
        self.m3u8_folder_path = m3u8_folder_path

    # 清理m3u8目录或创建
    @staticmethod
    def clear_m3u8(m3u8_folder_path):
        if not os.path.exists(m3u8_folder_path):
            os.makedirs(m3u8_folder_path)
        subs = os.listdir(m3u8_folder_path)
        for s in subs:
            file_path = os.path.join(m3u8_folder_path, s)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path, True)

    # 生成m3u8文件
    def generate_m3u8(self):
        m3u8_file_path = self.m3u8_folder_path + self.m3u8_name
        self.clear_m3u8(self.m3u8_folder_path)
        command = self.ffmpeg_path + ' -i ' + self.video_path + ' -hls_time 10 -hls_list_size 0 ' \
                  '-hls_segment_filename ' + m3u8_file_path[:m3u8_file_path.rfind('.')] + '_%05d.ts ' + m3u8_file_path
        command_output = self.run_command_and_get_output(command)
        check_equal = self.check_video_time(self.video_path, m3u8_file_path)
        if not check_equal:
            return command_output
        return 'success'

    # 获取ts文件列表
    def get_ts_list(self):
        m3u8_file_path = self.m3u8_folder_path + self.m3u8_name
        ts_list = []
        with open(m3u8_file_path, 'r') as file:
            for line in file.readlines():
                if line.find('.ts') > 0:
                    ts_list.append(line.strip())
        return ts_list


if __name__ == '__main__':
    result = HlsVideoUtil('lucene.mp4', 'lucene.m3u8', './lucene/').get_ts_list()
    print(result)
