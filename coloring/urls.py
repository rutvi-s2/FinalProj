from django.urls import path
from . import views

urlpatterns = [
  path('wasteless/<slug:username>/newlisting/', views.newlisting),
  path('wasteless/<slug:username>/friends/', views.friends),
  path('wasteless/<slug:username>/profile/mylistings/', views.mylistings),
  path('wasteless/<slug:username>/profile/claimed/', views.claimed),
  path('wasteless/<slug:username>/profile/saved/', views.saved),
  path('wasteless/<slug:username>/profile/', views.profile),
  path('wasteless/<slug:username>/', views.index),
  # path('wasteless/', views.index),
  path('', views.index)
]
