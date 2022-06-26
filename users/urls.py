from django.urls import path, include
from . import views as user_views
from django.contrib.auth import views as auth_views

from .views import ViewUser, ViewStaff

urlpatterns = [
    path('register/', user_views.Register.as_view(), name='register'),
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
    path('<pk>/update/', user_views.UpdateProfile.as_view(), name='update-profile'),
    path('<pk>/delete/', user_views.DeleteProfile.as_view(), name='delete-profile'),
    path('view_user/', ViewUser.as_view(), name='view-user'),
    path('view_staff/', ViewStaff.as_view(), name='view-staff'),
    path('', include('Hospital.urls')),

]
