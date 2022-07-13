from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from nurse.forms import DutyForm
from nurse.models import NurseDuty
from users.models import CustomUser


def is_admin(user):
    return CustomUser.objects.filter(username=user).filter(is_superuser=True)


class AssignDuty(SuccessMessageMixin, CreateView):
    """
    class for assign duty to  nurses.
    """
    form_class = DutyForm
    template_name = 'nurse/assign_duty.html'
    success_url = reverse_lazy('Hospital-home')
    success_message = 'Duty Assigned successfully to the staff'

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(AssignDuty, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')


class ViewDuty(ListView):
    """
    class for view the list of duty
    """
    model = NurseDuty
    template_name = 'nurse/view_duty.html'
    context_object_name = 'nurseduty'

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(ViewDuty, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')
