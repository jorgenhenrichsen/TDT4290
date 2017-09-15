from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
]
