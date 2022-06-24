from django.urls import path
from . import views
from .views import ViewAppointments

urlpatterns = [
    path('appointments/', views.BookAppointments.as_view(), name='book-appointments'),
    path('view/', ViewAppointments.as_view(), name='view-appointments'),
]
