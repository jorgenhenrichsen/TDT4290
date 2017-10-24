from django.conf.urls import url
from accounts import views
from accounts.views import register, user_login,user_logout, home,set_password_view,reset_password_mailer_view,display_users_view, edit_user_view
#make_club_admin_view
#activate_user

urlpatterns = [

    url(r'^adminPanel/', views.admin, name='home'),
    url(r'^home/admin/$', views.admin, name='home'),
    url(r'^home2/$', home),
    url(r'^register/$', register),
    url(r'^login2/$', user_login),
    url(r'^logout/$', user_logout),
    url(r'^brukere/$',display_users_view),
    #url(r'^activate/(?P<code>[a-z0-9].*)/$',activate_user),
    #url(r'^club_admin/(?P<code>[a-z0-9].*)/$', make_club_admin_view),
    url(r'^reset-password/(?P<code>[a-z0-9].*)/$', set_password_view),
    url(r'^glemt-passord/$', reset_password_mailer_view),
    url(r'^endre-bruker/(?P<id>[0-9].*)/$',edit_user_view)
]
