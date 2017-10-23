from django.conf.urls import url

from . import views

app_name = 'resultregistration'

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^lifter/(?P<pk>\d+)/$', views.lifter_detail, name='lifter_detail'),
    url(r'^lifter/new/$', views.add_new_lifter, name='add_new_lifter'),
    url(r'^judge/(?P<pk>\d+)/$', views.judge_detail, name='judge_detail'),
    url(r'^judge/new/$', views.add_new_judge, name='add_new_judge'),
    url(r'^staff/(?P<pk>\d+)/$', views.staff_detail, name='staff_detail'),
    url(r'^staff/new/$', views.add_new_staff, name='add_new_staff'),
    url(r'^resultregistration/$', views.result_registration, name="result_registration"),



    url(r'^resultregistration/group/new$', views.GroupFormView.as_view(), name='add_group'),
    url(r'^resultregistration/result/pending/new$', views.PendingResultFormView.as_view(), name='add_pending_result'),
    url(r'^resultregistration/competition/new/$', views.CompetitionFormView.as_view(), name='add_competition'),
    # url(r'^resultregistration/competition/new/register$', views.CompetitionFormView.as_view, name='add_competition'),
    url(r'^resultregistration/resultform/$', views.result_view, name='result_view'),
]