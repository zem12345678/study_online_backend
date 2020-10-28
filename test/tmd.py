import subprocess


def run_command_and_get_output(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process_result = process.stdout.read()
        return process_result.decode('utf-8', errors='ignore')
    except Exception as e:
        print(e)
        return ''


if __name__ == '__main__':
    result = run_command_and_get_output('ffmpeg -i  lucene.avi -c:v libx264 -s 1280x720 -pix_fmt yuv420p -b:a 63k -b:v 753k -r 18 lucene.mp4')
    print(result)
