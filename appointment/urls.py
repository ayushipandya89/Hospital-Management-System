from django.urls import path
from . import views
from . import views as user_views
from .views import ViewAppointments, ViewRooms, ViewAdmitPatient, SearchRoom, SearchAdmit, LoadTimeslots, \
    ViewDischargePatient, DischargeByDoctor, DischargebyAdminView

urlpatterns = [
    path('appointments/', views.BookAppointments.as_view(), name='book-appointments'),
    path('search_timeslot/', LoadTimeslots.as_view(), name='search_timeslot'),
    path('view_appointment/', ViewAppointments.as_view(), name='view-appointments'),
    path('<pk>/delete_appointment/', views.DeleteAppointmentView.as_view(), name='delete-appointments'),
    path('rooms/', views.EnterRoomData.as_view(), name='room'),
    path('search_room/', SearchRoom.as_view(), name='search_room'),
    path('view_rooms/', ViewRooms.as_view(), name='view-rooms'),
    path('admit/', views.EnterAdmitPatient.as_view(), name='admit-patient'),
    path('discharge_patient/', ViewDischargePatient.as_view(), name='discharge_patient_list'),
    path('search_admit/', SearchAdmit.as_view(), name='search_admit'),
    path('view_admit/', ViewAdmitPatient.as_view(), name='view-admit-patient'),
    path('<pk>/discharge/', user_views.DischargePatient.as_view(), name='discharge-patient'),
    path('view_not_dicharge/', DischargebyAdminView.as_view(), name='view-discharge-patient'),
    path('<int:pk>/discharge_request/', DischargeByDoctor.as_view(), name='discharge_by_doctor'),

]
