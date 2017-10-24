from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^new-user', views.UserFormView.as_view(), name='new-user'),
    url(r'^users', views.UserListView.as_view(), name='users-list'),
    url(r'^results-for-approval', views.ListOfResultsView.as_view(), name="result")
]