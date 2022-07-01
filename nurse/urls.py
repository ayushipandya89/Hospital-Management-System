from django.urls import path
from . import views
from .views import ViewDuty

urlpatterns = [
    path('duty/', views.AssignDuty.as_view(), name='duty'),
    path('view_duty/', ViewDuty.as_view(), name='view-duty'),

]
