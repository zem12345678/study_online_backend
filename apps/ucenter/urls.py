from django.conf.urls import url
from ucenter.views import SmsCodeViewSet, UserViewSet

urlpatterns = [
    url(r'^auth/code', SmsCodeViewSet.as_view({'post': 'create'})),
    url(r'^auth/register', UserViewSet.as_view({'post': 'create'})),
]
