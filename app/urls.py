from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('registers/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('alerts/', views.alerts, name="alerts"),
    path('alerts/new/', views.newalert, name="newalert"),
    path('alerts/edit/', views.alertsedit, name="editalerts"),
    path('schedules/new/', views.newlink, name="newlink"),
    path('schedules/edit/', views.editschedules, name="editschedules"),
    path('feedback/', views.feedback, name="feedback"),
    path('feedback/view/', views.feedbackview, name="feedbackview"),
    path('links/<pk>/', views.links, name="links"),
    path('contact/', views.contact, name="contact"),
    path('email/', views.email, name="email"), 
    path('delete/<pk>/', views.delete, name="delete"),
    path('overall/', views.overall),
    path('certificate/<pk>/', views.GenerateCertificate.as_view(), name="certificate"),
    path('ygfu36t63uyg4/report/', views.GenerateReport.as_view(), name="report"),
    path('alerts/massmail/<pk>/', views.masssendlink, name="massmail"),
]
