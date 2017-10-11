from django.conf.urls import url, include
from accounts import views

urlpatterns = [
    url(r'^adminPanel/', views.admin, name='home'),
    url(r'^admin/', views.admin, name='home'),
    url(r'', include('resultregistration.urls')),
]
