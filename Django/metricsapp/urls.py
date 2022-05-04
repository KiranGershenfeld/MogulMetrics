from django.urls import path

from . import views

urlpatterns = [
    path('api/all_livestreams', views.all_livestreams)
]