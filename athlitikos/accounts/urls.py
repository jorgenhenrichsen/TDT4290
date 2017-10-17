from django.conf.urls import url
from accounts import views
from accounts.views import register, user_login,user_logout, home, make_club_admin_view,reset_password_view,activate_user


urlpatterns = [
    url(r'^adminPanel/', views.admin, name='home'),
    url(r'^admin/', views.admin, name='home'),
    url(r'^home2/', home),
    url(r'^register/$', register),
    url(r'^login2/$', user_login),
    url(r'^logout/$', user_logout),
    url(r'^activate/(?P<code>[a-z0-9].*)/$',activate_user),
    url(r'^club_admin/(?P<code>[a-z0-9].*)/$', make_club_admin_view),
    url(r'^reset_password/(?P<code>[a-z0-9].*)/$', reset_password_view),
]
