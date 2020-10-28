import json
from datetime import datetime, timedelta
from django.db import transaction
from celery_tasks.main import app
from order.models import CzTask, CzTaskHis
from order.serializers import CzTaskHisSerializer
from learning.models import CzLearningCourse
from course.models import CourseMarket
from common import sys_dict


@app.task(bind=True, name='add')
def add(self, a, b):
    print('a + b = {}'.format(a+b))


@app.task(bind=True, name='choose_course_task', retry_kwargs={'max_retries': 3})
def choose_course_task(self):
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    tasks = CzTask.objects.filter(update_time__lte=one_minute_ago).order_by('update_time')[:10]
    for task in tasks:
        with transaction.atomic():
            targetv_task = CzTask.objects.filter(id=task.id, version=task.version).first()
            if targetv_task is not None:
                kwargs = json.loads(task.request_body)
                kwargs['task_id'] = targetv_task.id
                add_choose_course.delay(**kwargs)  # 发送添加选课消息
                targetv_task.update_time = datetime.now()
                targetv_task.version = targetv_task.version + 1
                targetv_task.save()


@app.task(bind=True, name='add_choose_course', retry_kwargs={'max_retries': 3})
def add_choose_course(self, task_id, user_id, course_id):
    task = CzTaskHis.objects.filter(id=task_id).first()
    if task is not None:
        return
    exists = CzLearningCourse.objects.filter(course_id= course_id, user_id=user_id).first()
    market = CourseMarket.objects.filter(id=course_id).first()
    if exists:
        exists.start_time = market.start_time
        exists.end_time = market.end_time
        exists.status = sys_dict.CHOOSE_COURSE_NONE
    else:
        exists = CzLearningCourse(
            course_id=course_id,
            user_id=user_id,
            charge=market.charge,
            price=market.price,
            valid=market.valid,
            start_time=market.start_time,
            end_time=market.end_time,
            status=sys_dict.CHOOSE_COURSE_NONE
        )
    exists.save()
    finish_choose_course.delay(task_id)  # 发送完成选课消息


@app.task(bind=True, name='finish_choose_course')
def finish_choose_course(self, task_id):
    task = CzTask.objects.get(id=task_id)
    task.delete_time = datetime.now()
    result = CzTaskHis.objects.create(**CzTaskHisSerializer(task).data)
    print(result)
    task.delete()
