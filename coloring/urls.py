from django.urls import path
from . import views

urlpatterns = [
  path('<slug:username>/newlisting/', views.newlisting),
  path('<slug:username>/friends/', views.friends),
  path('<slug:username>/', views.index),
  # path('wasteless/', views.index),
  path('', views.index)
]
