from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from constants import APPOINTMENT_SUCCESS_MSG, ROOM_SUCCESS_MSG, ADMIT_SUCCESS_MSG, DISCHARGE_SUCCESS_MSG, \
    APPOINTMENT_DELETE_MSG
from users.views import is_admin
from .forms import PatientAppointmentForm, PatientTimeslotsUpdate, CreateRoomForm, AdmitPatientForm, DischargeUpdateForm
from .models import Appointments, Room, Admit


def load_timeslots(request):
    fetch_staff = request.GET.get('staff_id')
    fetch_date = request.GET.get('date')
    print('fetch_date:', fetch_date)
    print('fetch_staff:', fetch_staff)
    fetch_time = Appointments.objects.filter(staff_id=fetch_staff).filter(date=fetch_date)
    print('fetch_time:', fetch_time)
    print(list(fetch_time.values('timeslot')), '................')
    return JsonResponse(list(fetch_time.values('timeslot')), safe=False)


class BookAppointments(View, SuccessMessageMixin):
    form_class = PatientAppointmentForm
    template_name = 'appointment/book_appointments.html'

    def get(self, request):
        form = PatientAppointmentForm()
        context = {'form': form}
        return render(request, 'appointment/book_appointments.html', context)

    def post(self, request, *args, **kwargs):
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, APPOINTMENT_SUCCESS_MSG)
            return redirect('Hospital-home')
        else:
            return render(request, self.template_name, {'form': form})


# class BookAppointments(SuccessMessageMixin, CreateView):
#     """
#     This class is for booking appointments.
#     """
#     form_class = PatientAppointmentForm
#     template_name = 'appointment/book_appointments.html'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse("appointment-timeslot", kwargs={'pk': self.object.pk})


class AppointmentTimeslotUpdate(SuccessMessageMixin, UpdateView):
    """
    This class is for adding the timeslot information.
    """
    form_class = PatientTimeslotsUpdate
    template_name = 'appointment/book_appointments_timeslots.html'
    success_message = APPOINTMENT_SUCCESS_MSG

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


class DeleteAppointmentView(View):
    """
    class for deleting appointment
    """
    http_method_names = ['delete']
    model = Appointments

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(DeleteAppointmentView, self).dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        fetch_id = kwargs["pk"]
        query = get_object_or_404(Appointments, pk=int(fetch_id))
        query.delete()
        messages.success(self.request, APPOINTMENT_DELETE_MSG)
        return render(self.request, 'Hospital/admin_home.html')


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
    success_url = reverse_lazy('Hospital-home')
    success_message = ROOM_SUCCESS_MSG

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(EnterRoomData, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')


class SearchRoom(View):
    """
    class for give data to ajax call for search user
    """

    def get(self, request):
        room = Room.objects.all().values_list('room_type', flat=True)
        room_list = list(room)
        return JsonResponse(room_list, safe=False)


class ViewRooms(View):
    """
    This class is for view rooms.
    """

    def get(self, request):
        all_data = Room.objects.all()
        context = {
            'all_data': all_data
        }
        return render(request, 'appointment/view_rooms.html', context)

    def post(self, request):
        search = request.POST['search']
        if search != " ":
            search = search.strip()
            user = Room.objects.filter(room_type__icontains=search)
            return render(request, 'appointment/view_rooms.html', {'data': user})
        else:
            return redirect('Hospital-home')

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(ViewRooms, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')


class EnterAdmitPatient(SuccessMessageMixin, CreateView):
    """
    class for adding admit patient data
    """
    form_class = AdmitPatientForm
    template_name = 'appointment/admit_patient.html'
    success_url = reverse_lazy('Hospital-home')
    success_message = ADMIT_SUCCESS_MSG

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(EnterAdmitPatient, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')


class ViewNotDischarged(View):

    def get(self, request):
        all_data = Admit.objects.filter(out_date__isnull=True)
        context = {
            'all_data': all_data
        }
        return render(request, 'appointment/view_not_discharge_patient.html', context)

    def post(self, request):
        search = request.POST['search']
        if search != " ":
            search = search.strip()
            user = Admit.objects.filter(patient__patient__username__icontains=search)
            return render(request, 'appointment/view_not_discharge_patient.html', {'data': user})
        else:
            return redirect('Hospital-home')

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(ViewNotDischarged, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')


class SearchAdmit(View):
    """
    class for give data to ajax call for search user
    """

    def get(self, request):
        patient = Admit.objects.all().values_list('patient__patient__username', flat=True)
        patient_list = list(patient)
        return JsonResponse(patient_list, safe=False)


class ViewAdmitPatient(ListView):
    def get(self, request):
        all_data = Admit.objects.all()
        context = {
            'all_data': all_data
        }
        return render(request, 'appointment/view_admit_patient.html', context)

    def post(self, request):
        search = request.POST['search']
        if search != " ":
            search = search.strip()
            user = Admit.objects.filter(patient__patient__username__icontains=search)
            return render(request, 'appointment/view_admit_patient.html', {'data': user})
        else:
            return redirect('Hospital-home')

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(ViewAdmitPatient, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')


class DischargePatient(UpdateView, SuccessMessageMixin):
    form_class = DischargeUpdateForm
    template_name = 'appointment/discharge_patient.html'
    success_url = reverse_lazy('Hospital-home')
    success_message = DISCHARGE_SUCCESS_MSG

    def get_queryset(self):
        query_set = Admit.objects.filter(id=self.kwargs['pk'])
        return query_set
