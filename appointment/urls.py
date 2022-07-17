from django.urls import path
from . import views
from . import views as user_views
from .views import ViewAppointments, ViewAllAppointments, ViewRooms, ViewAdmitPatient, \
    ViewNotDischarged, DeleteAppointmentView

urlpatterns = [
    path('appointments/', views.BookAppointments.as_view(), name='book-appointments'),
    path('search_timeslot/', views.load_timeslots, name='search_timeslot'),
    path('<pk>/appointment_timeslot/', user_views.AppointmentTimeslotUpdate.as_view(), name='appointment-timeslot'),
    path('view_appointment/', ViewAppointments.as_view(), name='view-appointments'),
    path('<pk>/delete_appointment/', views.DeleteAppointmentView.as_view(), name='delete-appointments'),
    path('view_all_appointment/', ViewAllAppointments.as_view(), name='view-all-appointments'),
    path('rooms/', views.EnterRoomData.as_view(), name='room'),
    path('view_rooms/', ViewRooms.as_view(), name='view-rooms'),
    path('admit/', views.EnterAdmitPatient.as_view(), name='admit-patient'),
    path('view_admit/', ViewAdmitPatient.as_view(), name='view-admit-patient'),
    path('<pk>/discharge/', user_views.DischargePatient.as_view(), name='discharge-patient'),
    path('view_dicharge/', ViewNotDischarged.as_view(), name='view-discharge-patient'),

]
