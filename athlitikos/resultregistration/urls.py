from django.conf.urls import url

from . import views

app_name = 'resultregistration'

urlpatterns = [
  url(r'^home/$', views.home, name='home'),
]