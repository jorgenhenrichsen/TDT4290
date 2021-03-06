from django.conf.urls import url

from . import views

app_name = 'resultregistration'

urlpatterns = [
    url(r'^lifter/(?P<pk>\d+)/$', views.lifter_detail, name='lifter_detail'),
    url(r'^lifter/new/$', views.add_new_lifter, name='add_new_lifter'),
    url(r'^judge/(?P<pk>\d+)/$', views.judge_detail, name='judge_detail'),
    url(r'^judge/new/$', views.add_new_judge, name='add_new_judge'),
    url(r'^club/new/$', views.add_new_club, name='add_new_club'),
    url(r'^resultregistration/$', views.v2_result_registration, name="result_registration"),
    # url(r'^resultregistration/from_excel$', views.v2_result_registration_with_context, name="result_registration_with_excel"),
    url(r'^resultregistration/edit/(?P<pk>\d+)/$', views.v2_edit_result, name='v2_edit_result'),
    url(r'^result/edit/(?P<pk>\d+)/$', views.edit_result, name='edit_result'),
    url(r'^result/approve/(?P<pk>\d+)/$', views.approve_group, name='approve_group'),
    url(r'^result/reject/(?P<pk>\d+)/$', views.reject_group, name='reject_group'),
    url(r'^result/send/(?P<pk>\d+)/$', views.send_group, name='send_group'),
    url(r'^result/delete/(?P<pk>\d+)/$', views.delete_group, name='delete_group'),
    url(r'^result/edit/clubofc/(?P<pk>\d+)/$', views.edit_result_clubofc, name='edit_result_clubofc'),
    # url(r'^resultregistration/group/new$', views.GroupFormView.as_view(), name='add_group'),
    url(r'^resultregistration/competition/new/$', views.add_new_competition, name='add_competition'),
    url(r'^resultregistration/resultform/$', views.result_view, name='result_view'),
    url(r'^resultregistration/groupform/$', views.group_registration, name='group_view'),
    # url(r'^resultregistration/result/pending/new$', views.PendingResultFormView.as_view(), name='add_pending_result'),
    url(r'^home/$', views.home, name='home'),
    url(r'^home/admin/$', views.home_admin, name='home_admin'),
    url(r'^home/clubofc/$', views.home_club_official, name='home_club_official'),
    url(r'^judges/$', views.list_all_judges, name="result_registration"),
    url(r'^merge-lifters/$', views.merge_find_two_lifters_view),
    url(r'^merge-lifters/merging$', views.merge_lifter_view),
    url(r'^result/change/(?P<pk>\d+)/$', views.change_result, name="change_result"),
    url(r'^result/change/clubofc/(?P<pk>\d+)/$', views.change_result_clubofc, name="change_result_clubofc"),
    url(r'^internationalresult/new/$', views.add_new_internationalresult,
        name='add_new_internationalresult'),
    url(r'^internationalresult/(?P<pk>\d+)/$', views.international_result_detail,
        name='international_result_detail'),
    url(r'^internationalgroup/new', views.add_new_international_group, name='new_international_group'),
    url(r'^internasjonal/konkurranse/ny', views.add_new_international_competition, name='new_international_competition'),
    url(r'autofill/result/$', views.get_result_autofill_data, name='get_result_autofill_data'),
    url(r'^resultregistration/fromexcel/$', views.result_from_excel, name='from_excel'),

]
