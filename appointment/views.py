from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from users.models import Staff
from .forms import PatientAppointmentForm, PatientTimeslotsUpdate, CreateRoomForm, AdmitPatientForm
from .models import Appointments, Room, Admit


class BookAppointments(SuccessMessageMixin, CreateView):
    """
    This class is for booking appointments.
    """
    form_class = PatientAppointmentForm
    template_name = 'appointment/book_appointments.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("appointment-timeslot", kwargs={'pk': self.object.pk})


class AppointmentTimeslotUpdate(SuccessMessageMixin, UpdateView):
    """
    This class is for adding the timeslot information.
    """
    form_class = PatientTimeslotsUpdate
    template_name = 'appointment/book_appointments_timeslots.html'
    success_message = "Your appointment was created successfully"

    def get_queryset(self):
        query_set = Appointments.objects.filter(id=self.kwargs['pk'])
        return query_set

    def get_success_url(self):
        return reverse("Hospital-home")


class ViewAppointments(ListView):
    """
    This class is for view patients appointment.
    """
    model = Appointments
    template_name = 'appointment/view_appointments.html'
    context_object_name = 'appointment'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user.id).order_by('-id')


class DeleteAppointmentView(DeleteView):
    """
    class for deleting appointments
    """
    model = Appointments
    template_name = 'appointment/appointment_confirm_delete.html'
    success_url = reverse_lazy('view-appointments')

    def test_func(self):
        appointments = self.get_object()
        if self.request.user == appointments.user:
            return True
        return False


class ViewAllAppointments(ListView):
    """
        This class is for view patients appointment by doctor.
    """
    model = Appointments
    template_name = 'appointment/view_appointments.html'
    context_object_name = 'appointment'


class EnterRoomData(SuccessMessageMixin, CreateView):
    """
    class for adding room data
    """
    form_class = CreateRoomForm
    template_name = 'appointment/create_rooms.html'
    success_url = reverse_lazy('Hospital-home   ')
    success_message = 'Your room was created.'

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(EnterRoomData, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser


class ViewRooms(ListView):
    """
    This class is for view rooms.
    """
    model = Room
    template_name = 'appointment/view_rooms.html'
    context_object_name = 'room'

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(ViewRooms, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser


class EnterAdmitPatient(SuccessMessageMixin, CreateView):
    """
    class for adding admit patient data
    """
    form_class = AdmitPatientForm
    template_name = 'appointment/admit_patient.html'
    success_url = reverse_lazy('Hospital-home')
    success_message = 'Admitted patient successfully'

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(EnterAdmitPatient, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser


class ViewAdmitPatient(ListView):
    """
    used for view all the admitted patient.
    """
    model = Admit
    template_name = 'appointment/view_admit_patient.html'
    context_object_name = 'admit'

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(ViewAdmitPatient, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser
