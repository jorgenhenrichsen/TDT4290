from django.conf.urls import url
from accounts.views import register, user_login, user_logout, set_password_view,\
    reset_password_mailer_view, display_users_view, edit_user_view

urlpatterns = [
    url(r'^register/$', register),
    url(r'^login/$', user_login),
    url(r'^logout/$', user_logout),
    url(r'^brukere/$', display_users_view),
    url(r'^reset-password/(?P<code>[a-z0-9].*)/$', set_password_view),
    url(r'^glemt-passord/$', reset_password_mailer_view),
    url(r'^endre-bruker/(?P<id>[0-9].*)/$', edit_user_view)
]
