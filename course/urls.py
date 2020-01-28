from django.urls import path, re_path, include

from course import views

urlpatterns = [
    re_path(r'^type_select$', views.type_select),
    re_path(r'^course_select$', views.course_select),
    re_path(r'^more_coursecmt$', views.more_coursecmt),
    re_path(r'^submit_coursecmt$', views.submit_coursecmt),
    re_path(r'^course_favorcmt$', views.course_favorcmt),
    re_path(r'^course_hotcmt$', views.course_hotcmt),
]