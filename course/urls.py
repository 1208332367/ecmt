from django.urls import path, re_path, include

from course import views

urlpatterns = [
    re_path(r'^listCourse$', views.listCourse),
    re_path(r'^course_teaching', views.course_teaching),
    re_path(r'^more_comment$', views.more_comment),
    re_path(r'^submit_comment$', views.submit_comment),
    re_path(r'^favor_comment$', views.favor_comment),
    re_path(r'^hot_comment$', views.hot_comment),
]