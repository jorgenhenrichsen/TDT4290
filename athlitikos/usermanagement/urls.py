from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^admin-startside/', views.admin, name='home'),
    url(r'^admin/', views.admin, name='home'),
   # url(r'^ny-bruker/', views.UserFormView(), name='home'),
    url(r'^register/', views.UserFormView.as_view(), name='register')
]