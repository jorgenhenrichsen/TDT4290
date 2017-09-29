from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^autocomplete/$', views.autocomplete, name='login'),
    url(r'^search/$', views.search_person_names)
]