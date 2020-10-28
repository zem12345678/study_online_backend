from django.conf.urls import url
from media.views import MediaUploadViewSet, MediaFileViewSet

urlpatterns = [
    url(r'^media/upload/register', MediaUploadViewSet.as_view({'post': 'register'})),
    url(r'^media/upload/checkchunk', MediaUploadViewSet.as_view({'post': 'checkchunk'})),
    url(r'^media/upload/uploadchunk', MediaUploadViewSet.as_view({'post': 'uploadchunk'})),
    url(r'^media/upload/mergechunks', MediaUploadViewSet.as_view({'post': 'mergechunk'})),
    url(r'^media/file/list/(?P<page>\d+)/(?P<size>\d+)', MediaFileViewSet.as_view({'get': 'list'})),
]
