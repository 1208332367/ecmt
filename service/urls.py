
from django.conf.urls import url
from django.urls import include, re_path

from . import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^upload/', include('upload.urls')),
    url(r'^course/', include('course.urls')),
    re_path(r'^user/', include('user.urls')),
]
