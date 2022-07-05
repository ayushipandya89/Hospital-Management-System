from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .forms import UserRegisterForm, UserUpdateForm, PatientRegistrationForm, StaffUpdateForm, FeedbackForm, \
    EmergencyForm, MedicineForm, MedicineUpdateForm, PrescriptionForm, PrescriptionUpdateForm

from .models import CustomUser, Patient, Staff, Feedback, Emergency, Medicine, Prescription


class Register(SuccessMessageMixin, CreateView):
    """
    This class is for user registration.
    """
    form_class = UserRegisterForm
    patient_form_class = PatientRegistrationForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_obj = form.save(commit=True)
            if user_obj.role == 'P':
                patient = Patient.objects.create(patient=user_obj)
                patient.save()
                messages.success(request, 'Patient Profile created successfully')
            if user_obj.role == 'D' or user_obj == 'N':
                staff = Staff.objects.create(staff=user_obj)
                staff.save()
                messages.success(request, 'Profile created successfully')
            if request.user.is_superuser:
                return redirect('Hospital-home')
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})


class UpdateProfile(SuccessMessageMixin, UpdateView):
    """
    This class is for update the profile information.
    """
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    success_message = "Your profile was updated successfully"

    def get_queryset(self):
        query_set = CustomUser.objects.filter(id=self.kwargs['pk'])
        return query_set

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("update-profile", kwargs={"pk": pk})


class DeleteProfile(SuccessMessageMixin, DeleteView):
    """
    This class is for delete the user profile.
    """
    model = CustomUser
    success_url = "/"

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.username:
            return True
        return False


class ViewUser(ListView):
    """
    class for view the list of customuser
    """
    model = CustomUser
    template_name = 'users/view_user.html'
    context_object_name = 'users'

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(ViewUser, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser


class ViewStaff(ListView):
    """
    class for view the list of customuser
    """
    model = Staff
    template_name = 'users/view_staff.html'
    context_object_name = 'staff'

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(ViewStaff, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser


class UpdateStaffProfile(SuccessMessageMixin, UpdateView):
    """
    This class is for update the profile information of staff.
    """
    form_class = StaffUpdateForm
    template_name = 'users/staff_update.html'
    success_message = "Your staff profile was updated successfully"

    def get_queryset(self, *args, **kwargs):
        query_set = Staff.objects.filter(id=self.kwargs['pk'])
        query = get_object_or_404(Staff, id=self.kwargs.get('pk'))
        return query_set

    def form_valid(self, form, *args, **kwargs):
        data = self.request.POST
        fetch_speciality = data.get('speciality')
        fetch_pk = get_object_or_404(Staff, id=self.kwargs.get('pk'))
        query = CustomUser.objects.filter(username=fetch_pk).values_list('role', flat=True)
        if query[0] == 'N' and fetch_speciality != 'Nurse':
            messages.error(self.request, f"you are nurse you can not choose another speciality...please choose nurse "
                                         f"as speciality")
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return reverse("view-staff")


class EnterFeedback(CreateView, SuccessMessageMixin):
    form_class = FeedbackForm
    template_name = 'users/feedback.html'

    def get_queryset(self):
        query_set = CustomUser.objects.filter(id=self.kwargs['pk'])
        print(query_set)
        return query_set

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(EnterFeedback, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, f"you have successfully submitted your feedback ")
        return reverse("Hospital-home")


class ViewFeedback(ListView):
    """
    class for view the list of feedback
    """
    model = Feedback
    template_name = 'users/view_feedback.html'
    context_object_name = 'feedback'

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(ViewFeedback, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser


class PatientPrescription(CreateView, SuccessMessageMixin):
    """
    class used for adding patient prescription
    """
    form_class = PrescriptionForm
    template_name = 'users/prescription.html'

    def form_valid(self, form):
        # query = Staff.objects.filter(staff_id=self.request.user).values_list('id', flat=True)
        a = self.request.user.id
        fetch = Staff.objects.filter(staff=a).first()
        form.instance.staff_id = fetch.id
        return super(PatientPrescription, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, f"You have successfully submitted prescription ")
        return reverse("view-prescription")

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(PatientPrescription, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return request.user.role == 'D'


class PrescriptionUpdate(SuccessMessageMixin, UpdateView):
    """
    This class is for update the profile information.
    """
    form_class = PrescriptionUpdateForm
    template_name = 'users/prescription_update.html'
    success_message = "Your prescription was updated successfully"

    def get_queryset(self):
        query_set = Prescription.objects.filter(id=self.kwargs['pk'])
        return query_set

    def get_success_url(self):
        return reverse('view-prescription')


class ViewPrescription(ListView):
    """
    class for view the list of prescription
    """
    model = Prescription
    template_name = 'users/view_prescription.html'
    context_object_name = 'prescription'

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(ViewPrescription, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return request.user.role == 'D'


class EmergencyCase(CreateView, SuccessMessageMixin):
    """
    class used for adding emergency case
    """
    form_class = EmergencyForm
    template_name = 'users/emergency.html'

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(EmergencyCase, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser

    def get_success_url(self):
        messages.success(self.request, f"You have successfully added emergency case")
        return reverse("Hospital-home")


class ViewEmergency(ListView):
    """
    class for view the list of emergency cases
    """
    model = Emergency
    template_name = 'users/view_emergency.html'
    context_object_name = 'emergency'

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(ViewEmergency, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser


class AddMedicine(CreateView, SuccessMessageMixin):
    """
    class for adding medicines
    """
    form_class = MedicineForm
    template_name = 'users/add_medicine.html'

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(AddMedicine, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return request.user.role == 'D'

    def get_success_url(self):
        messages.success(self.request, f"Medicine added successfully")
        return reverse("Hospital-home")


class ViewMedicine(ListView):
    """
    class for view the list of medicine
    """
    model = Medicine
    template_name = 'users/view_medicine.html'
    context_object_name = 'medicine'

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(ViewMedicine, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return request.user.role == 'D'


class MedicineUpdate(SuccessMessageMixin, UpdateView):
    """
    This class is for update the medicine information.
    """
    form_class = MedicineUpdateForm
    template_name = 'users/medicine_update.html'
    success_message = "Your medicine was updated successfully"

    def get_queryset(self):
        query_set = Medicine.objects.filter(id=self.kwargs['pk'])
        return query_set

    def get_success_url(self):
        return reverse('view-medicine')

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(MedicineUpdate, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return request.user.role == 'D'
