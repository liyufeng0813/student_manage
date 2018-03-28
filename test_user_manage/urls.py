"""test_user_manage URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from app_01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.Login.as_view()),
    url(r'^logout', views.logout),
    url(r'^index', views.index),
    url(r'^register', views.register),

    url(r'^classes', views.classes),
    url(r'^class_add', views.classes_add),
    url(r'^edit_classes', views.edit_classes),
    url(r'^remove_classes', views.remove_classes),

    url(r'^student_form_add', views.student_form_add),
    url(r'^student_ajax_add', views.student_ajax_add),
    url(r'^student_edit', views.student_edit),
    url(r'^student_delete', views.student_delete),
    url(r'^student_detail', views.student_detail),
    url(r'^student', views.student),

    url(r'^teacher_form_add', views.teacher_form_add),
    url(r'^teacher_form_edit-(?P<tid>\d+)', views.teacher_form_edit),
    url(r'^teacher_ajax_delete', views.teacher_ajax_delete),
    url(r'^teacher', views.teacher),

    url(r'^upload_ajax', views.upload_ajax),
    url(r'^upload', views.upload),
]
