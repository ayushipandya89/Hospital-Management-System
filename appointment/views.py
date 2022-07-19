from datetime import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from constants import APPOINTMENT_SUCCESS_MSG, ROOM_SUCCESS_MSG, ADMIT_SUCCESS_MSG, DISCHARGE_SUCCESS_MSG, \
    APPOINTMENT_DELETE_MSG
from users.models import Patient, CustomUser
from users.views import is_admin
from .forms import PatientAppointmentForm, CreateRoomForm, AdmitPatientForm, DischargeUpdateForm
from .models import Appointments, Room, Admit


class LoadTimeslots(View):
    """
    class for give data to ajax call for loading available  timeslots  from database
    """
    def get(self, request):
        fetch_staff = request.GET.get('staff_id')
        fetch_date = request.GET.get('date')
        fetch_time = Appointments.objects.filter(staff_id=fetch_staff).filter(date=fetch_date)
        user_data = []
        time_slot_choices = []
        time_list = []
        for i in fetch_time:
            time_list.append(i.timeslot)
        time = datetime.now()
        date = datetime.now().date()
        current_time = time.strftime("%H:%M:%S")
        if str(fetch_date) == str(date):
            for i in range(9, 20):
                if i > int(current_time.split(':')[0]):
                    if i != 12:
                        user_data.append(i)
                        time_slot_choices.append(f"{i}:00")
        else:
            for i in range(9, 20):
                if i != 12:
                    user_data.append(i)
                    time_slot_choices.append(f"{i}:00")
        time_list = sorted(time_list)
        time_slot_choices = sorted(time_slot_choices)
        b = set(time_slot_choices).difference(time_list)
        b = list(sorted(b))
        return JsonResponse(b, safe=False)


class BookAppointments(View, SuccessMessageMixin):
    """
    class for booking appointment
    """
    form_class = PatientAppointmentForm
    template_name = 'appointment/book_appointments.html'

    def get(self, request):
        form = PatientAppointmentForm()
        context = {'form': form}
        return render(request, 'appointment/book_appointments.html', context)

    def post(self, request, *args, **kwargs):
        print(self.request.user)
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            fetch_patient = Patient.objects.filter(patient_id=self.request.user).first()
            print(fetch_patient.patient_id)
            form.instance.user_id = CustomUser.objects.filter(id=fetch_patient.patient_id).first().id
            appointment_form = form.save(commit=False)
            appointment_form.save()
            messages.success(request, APPOINTMENT_SUCCESS_MSG)
            return redirect('Hospital-home')
        else:
            return render(request, self.template_name, {'form': form})


class ViewAppointments(ListView):
    """
    This class is for view patients appointment.
    """
    model = Appointments
    template_name = 'appointment/view_appointments.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        staff_query = Appointments.objects.filter(staff__staff__username=self.request.user).order_by('id')
        patient_query = Appointments.objects.filter(user__username=self.request.user).order_by('id')
        print(staff_query)
        print(patient_query)
        if staff_query:
            return staff_query
        elif patient_query:
            return patient_query
        else:
            return Appointments.objects.all()


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
    class for give data to ajax call for search rooms
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
    """
    class for display list of admitted patient who are not discharged yet
    """

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
    class for give data to ajax call for search admit user
    """

    def get(self, request):
        patient = Admit.objects.all().values_list('patient__patient__username', flat=True)
        patient_list = list(patient)
        return JsonResponse(patient_list, safe=False)


class ViewAdmitPatient(View):
    """
    class for view list of admitted patient
    """

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
    """
    class for discharge patient from hospital
    """
    form_class = DischargeUpdateForm
    template_name = 'appointment/discharge_patient.html'

    def get_queryset(self):
        query_set = Admit.objects.filter(id=self.kwargs['pk'])
        return query_set

    def get_success_url(self):
        messages.success(self.request, DISCHARGE_SUCCESS_MSG)
        return reverse("Hospital-home")


class ViewDischargePatient(View):
    """
    class for displaying list of discharge patient
    """
    def get(self, request):
        all_data = Admit.objects.filter(out_date__isnull=False)
        context = {
            'all_data': all_data
        }
        return render(request, 'appointment/view_discharge_patient.html', context)

    def post(self, request):
        search = request.POST['search']
        if search != " ":
            search = search.strip()
            user = Admit.objects.filter(patient__patient__username__icontains=search)
            return render(request, 'appointment/view_discharge_patient.html', {'data': user})
        else:
            return redirect('Hospital-home')

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(ViewDischargePatient, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

