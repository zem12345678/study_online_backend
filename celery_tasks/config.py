from kombu import Queue, Exchange
import os
from datetime import timedelta
from cz_study import settings
from celery.schedules import crontab
# 指定rabbitmq作为celery的队列
# BROKER_URL = "amqp://test:test@2018@172.17.0.98:5672//"
BROKER_URL = "amqp://guest:guest@localhost:5672//"
# celery时区相关配置
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False

CELERY_QUEUES = (
    Queue(settings.QUEUE_CMS_POST_PAGE,
          exchange=Exchange(settings.EX_CMS_POST_PAGE, 'direct'),
          routing_key=settings.ROUTING_KEY_CMS_POST_PAGE),
    Queue(settings.QUEUE_MEDIA_VIDEO_PROCESSOR,
          exchange=Exchange(settings.EX_MEDIA_PROCESSTASK, 'direct'),
          routing_key=settings.ROUTINGKEY_MEDIA_VIDEO),
    Queue(settings.QUEUE_ADD_CHOOSE_COURSE,
          exchange=Exchange(settings.EX_ADD_CHOOSE_COURSE, 'direct'),
          routing_key=settings.ROUTING_KEY_ADD_CHOOSE_COURSE_KEY),
    Queue(settings.QUEUE_FINISH_ADD_CHOOSE_COURSE,
          exchange=Exchange(settings.EX_ADD_CHOOSE_COURSE, 'direct'),
          routing_key=settings.ROUTING_KEY_FINISH_ADD_CHOOSE_COURSE),
    Queue('celery', routing_key='celery'),
)
CELERY_ROUTES = {
    'post_page': {
        'queue': settings.QUEUE_CMS_POST_PAGE,
        'routing_key': settings.ROUTING_KEY_CMS_POST_PAGE
    },
    'media_process': {
        'queue': settings.QUEUE_MEDIA_VIDEO_PROCESSOR,
        'routing_key': settings.ROUTINGKEY_MEDIA_VIDEO
    },
    'add_choose_course': {
        'queue': settings.QUEUE_ADD_CHOOSE_COURSE,
        'routing_key': settings.ROUTING_KEY_ADD_CHOOSE_COURSE_KEY
    },
    'finish_choose_course': {
        'queue': settings.QUEUE_FINISH_ADD_CHOOSE_COURSE,
        'routing_key': settings.ROUTING_KEY_FINISH_ADD_CHOOSE_COURSE
    }
}
CELERYBEAT_SCHEDULE = {
    # 'add-every-30-seconds': {
    #     'task': 'add',
    #     'schedule': 30,
    #     'args': (15, 15)
    # },
    # 'add-every-1-minute-10-seconds': {
    #     'task': 'add',
    #     'schedule': timedelta(minutes=1, seconds=10),
    #     'args': (1, 10)
    # },
    # 'add-config-by-crontab': {
    #     'task': 'add',
    #     'schedule': crontab(hour=19, minute=58, day_of_week=0),
    #     'args': (16, 16)
    # },
    'choose-course': {
        'task': 'choose_course_task',
        'schedule': crontab()
    }
}
