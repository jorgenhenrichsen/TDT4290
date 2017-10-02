from django.conf.urls import url

from . import views

app_name = 'public'

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^search/lifter/$', views.search_for_lifter, name='search_for_lifter'),
]