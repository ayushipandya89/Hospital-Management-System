from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import UserRegisterForm, UserUpdateForm, PatientRegistrationForm
from .models import CustomUser, Patient, Staff


class Register(SuccessMessageMixin, CreateView):
    """
    This class is for user registration.
    """
    form_class = UserRegisterForm
    patient_form_class = PatientRegistrationForm
    template_name = 'users/register.html'
    success_url = '../login'

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
                messages.success(request, 'Profile created successfully')
            if user_obj.role == 'D' or user_obj == 'N':
                staff = Staff.objects.create(staff=user_obj)
                staff.save()
                messages.success(request, 'Profile created successfully')
            return redirect('login')
        else:
            messages.error(request, "Error. Please enter correct data")
            return redirect('register')


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
