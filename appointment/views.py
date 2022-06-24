from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from .forms import PatientAppointmentForm
from .models import Appointments


class BookAppointments(SuccessMessageMixin, CreateView):
    """
    This class is for booking appointments.
    """
    form_class = PatientAppointmentForm
    template_name = 'appointment/book_appointments.html'
    success_url = '/'
    success_message = 'Your appointment is booked'


class ViewAppointments(ListView):
    model = Appointments
    template_name = 'appointment/view_appointments.html'
    context_object_name = 'appointment'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    # @method_decorator(user_is_doctor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user.id).order_by('-id')
#nkldsn