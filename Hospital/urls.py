from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Hospital-home'),
    path('about/', views.about, name='Hospital-about'),
]
