from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from order import admin_views

router = SimpleRouter()
router.register('task', admin_views.CzTaskViewSet)
router.register('task_his', admin_views.CzTaskHisViewSet)

urlpatterns = [
    url(r'admin/', include(router.urls)),
]
