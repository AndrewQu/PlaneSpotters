from django.conf.urls import url
from PlaneSighting import views
 
urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^add', views.add, name='add_sighting'),
   url(r'^save', views.save_sighting, name='save_sighting'),
   url(r'^service', views.service, name='service'),
]