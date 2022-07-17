from django.urls import path
from . import views
from .views import ViewDuty, SearchDuty

urlpatterns = [
    path('duty/', views.AssignDuty.as_view(), name='duty'),
    path('view_duty/', ViewDuty.as_view(), name='view-duty'),
    path('search_duty/', SearchDuty.as_view(), name='search_duty'),

]
