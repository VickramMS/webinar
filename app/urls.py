from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('report/', views.report, name="report"),
    path('alerts/', views.alerts, name="alerts"),
    path('alerts/new/', views.newalert, name="newalert"),
    path('alerts/edit/', views.alertsedit, name="editalerts"),
    path('schedules/new/', views.newlink, name="newlink"),
    path('schedules/edit/', views.editschedules, name="editschedules"),
]
