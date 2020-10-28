from django.conf.urls import url
from filesystem.views import FileSystemView

urlpatterns = [
    url(r'filesystem/upload', FileSystemView.as_view())
]
