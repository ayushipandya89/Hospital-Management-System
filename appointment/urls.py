from django.urls import path
from . import views
from . import views as user_views
from .views import ViewAppointments, DeleteAppointmentView, ViewDoctorsAppointments

urlpatterns = [
    path('appointments/', views.BookAppointments.as_view(), name='book-appointments'),
    path('<pk>/appointment_timeslot/', user_views.AppointmentTimeslotUpdate.as_view(), name='appointment-timeslot'),
    path('view_appointment/', ViewAppointments.as_view(), name='view-appointments'),
    path('<pk>/delete_appointment/', DeleteAppointmentView.as_view(), name='delete-appointments'),
    path('view_doc_appointment/', ViewDoctorsAppointments.as_view(), name='view-doc-appointments'),

]
