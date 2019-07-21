from django.urls import path

from .views import (
    AppSessionView, FormsView, HomeView
)

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('forms', FormsView.as_view(), name='forms'),
    path('app-session/', AppSessionView.as_view(), name='app_session'),
]
