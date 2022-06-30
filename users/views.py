from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .forms import UserRegisterForm, UserUpdateForm, PatientRegistrationForm, StaffUpdateForm
from .models import CustomUser, Patient, Staff


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

    def get_queryset(self):
        query_set = Staff.objects.filter(id=self.kwargs['pk'])
        return query_set

    def get_success_url(self):
        return reverse("view-staff")
