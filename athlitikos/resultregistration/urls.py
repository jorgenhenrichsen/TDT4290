from django.conf.urls import url

from . import views

app_name = 'resultregistration'

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^lifter/(?P<pk>\d+)/$', views.lifter_detail, name='lifter_detail'),
    url(r'^lifter/new/$', views.add_new_lifter, name='add_new_lifter'),
]