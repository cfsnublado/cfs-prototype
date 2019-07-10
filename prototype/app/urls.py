from django.urls import path

from .views import (
    FormsView, HomeView
)

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('forms', FormsView.as_view(), name='forms'),
]
