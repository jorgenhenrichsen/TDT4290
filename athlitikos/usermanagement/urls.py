from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^admin-startside/', views.admin, name='home'),
    url(r'^admin/', views.admin, name='home'),
    url(r'^ny-bruker/', views.create_new_user, name='home'),
]