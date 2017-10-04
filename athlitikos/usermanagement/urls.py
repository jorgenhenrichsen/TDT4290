from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^adminPanel/', views.admin, name='home'),
    url(r'^admin/', views.admin, name='home')
]