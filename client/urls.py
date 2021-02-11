from django.contrib import admin
from django.urls import path
from .views import ListCreateClient, GetUpdateDeleteClientInfo, CreateClientProject

urlpatterns = [
    path('clients/', ListCreateClient.as_view()),
    path('clients/<int:pk>', GetUpdateDeleteClientInfo.as_view()),
    path('clients/<int:id>/projects/',CreateClientProject.as_view())
]