"""cz_study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import booktest.urls
import cms.urls
import course.urls
import filesystem.urls
import search.urls
import media.urls
import learning.urls
import ucenter.urls
import order.urls
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(booktest.urls)),
    url(r'^', include(cms.urls)),
    url(r'^', include(course.urls)),
    url(r'^', include(filesystem.urls)),
    url(r'^', include(search.urls)),
    url(r'^', include(media.urls)),
    url(r'^', include(learning.urls)),
    url(r'^', include(ucenter.urls)),
    url(r'^', include(order.urls)),
    url('auth/userlogin', obtain_jwt_token)
]
