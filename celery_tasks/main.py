from celery import Celery
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
# 读取django项目的配置
os.environ["DJANGO_SETTINGS_MODULE"] = "cz_study.settings"

# 创建celery对象
app = Celery('cz_study')

# 加载配置
app.config_from_object('celery_tasks.config')

# 加载可用的任务
app.autodiscover_tasks([
    'celery_tasks.cms',
    'celery_tasks.media',
    'celery_tasks.course',
])
