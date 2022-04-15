from django.urls import path
from . import views

urlpatterns = [
  path('newlisting/', views.newlisting),
  path('coloring/<slug:authorname>/', views.index),
  path('coloring/', views.index), 
  path('', views.index),
]
