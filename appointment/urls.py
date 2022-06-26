from django.urls import path
from . import views
from .views import ViewAppointments, DeleteAppointmentView, ViewDoctorsAppointments

urlpatterns = [
    path('appointments/', views.BookAppointments.as_view(), name='book-appointments'),
    path('view_appointment/', ViewAppointments.as_view(), name='view-appointments'),
    path('<pk>/delete_appointment/', DeleteAppointmentView.as_view(), name='delete-appointments'),
    path('view_doc_appointment/', ViewDoctorsAppointments.as_view(), name='view-doc-appointments'),

]
