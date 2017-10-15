from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^admin-startside/', views.admin, name='adminpanel'),
    url(r'^admin/', views.admin, name='home'),
    url(r'^ny-bruker', views.UserFormView.as_view(), name='register')
]