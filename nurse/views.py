from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from nurse.forms import DutyForm
from nurse.models import NurseDuty


class AssignDuty(SuccessMessageMixin, CreateView):
    """
    class for assign duty to  nurses.
    """
    form_class = DutyForm
    template_name = 'nurse/assign_duty.html'
    success_url = reverse_lazy('Hospital-home')
    success_message = 'Duty Assigned successfully to the staff'

    # def form_valid(self, form, *args, **kwargs):
    #     data = self.request.POST
    #     fetch_patient = data.get('patient')
    #     print(fetch_patient)
    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(AssignDuty, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser


class ViewDuty(ListView):
    """
    class for view the list of duty
    """
    model = NurseDuty
    template_name = 'nurse/view_duty.html'
    context_object_name = 'nurseduty'

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_permissions(request):
            return super(ViewDuty, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')

    def user_has_permissions(self, request):
        return self.request.user.is_superuser
