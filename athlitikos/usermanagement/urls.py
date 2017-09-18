from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^lifter/new', views.add_new_lifter, name='add_new_lifter'),
]
