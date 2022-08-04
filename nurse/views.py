from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from constants import DUTY_ASSIGN_MSG
from nurse.forms import DutyForm
from nurse.models import NurseDuty
from users.views import is_admin, is_nurse


class AssignDuty(SuccessMessageMixin, CreateView):
    """
    class for assign duty to  nurses.
    """
    form_class = DutyForm
    template_name = 'nurse/assign_duty.html'
    success_url = reverse_lazy('Hospital-home')
    success_message = DUTY_ASSIGN_MSG

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(AssignDuty, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')


class SearchDuty(View):
    """
    class for give data to ajax call for search user
    """

    def get(self, request):
        room = NurseDuty.objects.all().values_list('staff__staff__username', flat=True)
        room_list = list(room)
        return JsonResponse(room_list, safe=False)


class ViewDuty(View):
    """
    class for view the list of duty
    """

    def get(self, request):
        user = NurseDuty.objects.filter(staff__staff__username=self.request.user).order_by('id')
        if user:
            context = {
                'all_data': user
            }
            return render(request, 'nurse/view_duty.html', context)
        else:
            all_data = NurseDuty.objects.all().order_by('id')
            context = {
                'all_data': all_data
            }
            return render(request, 'nurse/view_duty.html', context)

    def post(self, request):
        fetch_search = request.POST['search']
        if fetch_search != " ":
            search = fetch_search.strip()
            user = NurseDuty.objects.filter(staff__staff__username__icontains=search).order_by('id')
            return render(request, 'nurse/view_duty.html', {'data': user})
        else:
            return redirect('Hospital-home')

    def dispatch(self, request, *args, **kwargs):
        if is_admin(user=self.request.user):
            return super(ViewDuty, self).dispatch(
                request, *args, **kwargs)
        elif is_nurse(user=self.request.user):
            return super(ViewDuty, self).dispatch(
                request, *args, **kwargs)
        return render(request, 'appointment/not_admin.html')
