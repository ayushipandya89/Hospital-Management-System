from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from .forms import PatientAppointmentForm, PatientTimeslotsUpdate
from .models import Appointments


class BookAppointments(SuccessMessageMixin, CreateView):
    """
    This class is for booking appointments.
    """
    form_class = PatientAppointmentForm
    template_name = 'appointment/book_appointments.html'

    # success_url = '/'
    # success_message = 'Your appointment is booked'

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
        print(query_set)
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
    # @method_decorator(user_is_doctor)
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


class ViewDoctorsAppointments(ListView):
    """
        This class is for view patients appointment by doctor.
    """
    model = Appointments
    template_name = 'appointment/view_appointments.html'
    context_object_name = 'appointment'
