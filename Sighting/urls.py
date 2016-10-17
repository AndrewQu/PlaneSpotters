﻿from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^add/$', views.add, name='add_sighting'),
   url(r'^add/service/$', views.service, name='service'),
   url(r'^add/uploadfile/$', views.uploadfile, name='uploadfile'),
]
