from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('subject/<int:id>/', views.subject, name="subject"),
]