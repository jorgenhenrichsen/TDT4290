from django.conf.urls import url

from . import views

app_name = 'public'

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^search/lifter/$', views.search_for_lifter, name='search_for_lifter'),
    url(r'^search/club/$', views.search_for_clubs, name='search_for_clubs'),
    url(r'^search/weight-classes/$', views.get_available_weight_classes, name='get_available_weight_classes'),
    url(r'^search/age-groups/$', views.get_age_groups, name='get_age_groups'),
    url(r'^search/report.pdf$', views.generate_report, name='generate_report'),
    url(r'^search/report.csv$', views.generate_csv_report, name='generate_csv_report'),
    url(r'^search/competitions/$', views.search_for_competitions, name='search_for_competitions'),
    url(r'^autocomplete/age_groups/$', views.autocomplete_age_groups, name='autocomplete_age_groups'),
    url(r'^search/group/(?P<pk>\d+)/$', views.preview_group, name='preview_group'),
    url(r'^$', views.front_page, name='front_page'),
]
