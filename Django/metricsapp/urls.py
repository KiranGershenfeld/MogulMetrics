from django.urls import path

from . import views

urlpatterns = [
    path('api/all_livestreams', views.all_livestreams),
    path('api/video_lifecycle', views.video_lifecycle),
    path('api/is_live', views.is_live),
    path('api/stream_table', views.stream_table)

]