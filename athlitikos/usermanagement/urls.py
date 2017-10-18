from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^admin-panel/', views.admin, name='adminpanel'),
    url(r'^admin/', views.admin, name='home'),
    url(r'^new-user', views.UserFormView.as_view(), name='register')
]