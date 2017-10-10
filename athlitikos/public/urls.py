from django.conf.urls import url

from . import views

app_name = 'public'

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^search/lifter/$', views.search_for_lifter, name='search_for_lifter'),
    url(r'^search/club/$', views.search_for_clubs, name='search_for_clubs'),
    url(r'^search/results/$', views.search_for_results, name='search_for_results'),
]