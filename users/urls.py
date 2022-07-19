from django.urls import path, include
from . import views as user_views, views
from django.contrib.auth import views as auth_views

from .views import ViewUser, ViewStaff, ViewFeedback, ViewEmergency, ViewPrescription, BillView, ViewMedicine, \
    SearchMedicine, SearchStaff, SearchEmergency, SearchFeedback, ViewTodayAppointment

urlpatterns = [
    path('register/', user_views.Register.as_view(), name='register'),
    path('add_role/', user_views.AddRole.as_view(), name='add_role'),
    path('add_speciality/', user_views.AddSpeciality.as_view(), name='add_speciality'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('<pk>/update_staff/', user_views.UpdateStaffProfile.as_view(), name='update-staff-profile'),
    path('<pk>/update/', user_views.UpdateProfile.as_view(), name='update-profile'),
    path('<pk>/delete/', user_views.DeleteProfile.as_view(), name='delete-profile'),
    path('search_user/', SearchStaff.as_view(), name='search_user'),
    path('view_user/', ViewUser.as_view(), name='view-user'),
    path('search_staff/', SearchStaff.as_view(), name='search_staff'),
    path('view_staff/', ViewStaff.as_view(), name='view-staff'),
    path('prescription/', user_views.PatientPrescription.as_view(), name='prescription'),
    path('view_prescription/', ViewPrescription.as_view(), name='view-prescription'),
    path('<pk>/update_prescription/', user_views.PrescriptionUpdate.as_view(), name='update-prescription'),
    path('emergency/', user_views.EmergencyCase.as_view(), name='emergency'),
    path('view_emergency/', ViewEmergency.as_view(), name='view-emergency'),
    path('search_emergency/', SearchEmergency.as_view(), name='search_emergency'),
    path('medicine/', user_views.AddMedicine.as_view(), name='add-medicine'),
    path('<pk>/update_medicine/', user_views.MedicineUpdate.as_view(), name='update-medicine'),
    path('search/', SearchMedicine.as_view(), name='search-medicine'),
    path('view_medicine/', ViewMedicine.as_view(), name='view-medicine'),
    path('create_bill/', user_views.CreateBill.as_view(), name='create-bill'),
    path('view_bill/', BillView.as_view(), name='view-bill'),
    path('bill/<pk>', views.BillDetailView.as_view(), name='bill-detail'),
    path('feedback/', user_views.EnterFeedback.as_view(), name='feedback'),
    path('search_feedback/', SearchFeedback.as_view(), name='search_feedback'),
    path('view_feedback/', ViewFeedback.as_view(), name='view-feedback'),
    path('view_todays_appointment/', ViewTodayAppointment.as_view(), name='view_todays_appointment'),
    path('', include('Hospital.urls')),

]
