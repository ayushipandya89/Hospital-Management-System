from django.shortcuts import render
from users.models import Staff


def home(request):
    """
    This function is for home page of hospital management system.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'Hospital/admin_home.html')
        else:
            if request.user.role_id == 2:
                return render(request, 'Hospital/patient_home.html')
            else:
                fetch_id = request.user.id
                is_user_approved = Staff.objects.filter(staff=fetch_id).filter(is_approve=True)
                print(is_user_approved)
                if is_user_approved:
                    if request.user.role_id == 3:
                        return render(request, 'Hospital/nurse_home.html')
                    else:
                        return render(request, 'Hospital/doc_home.html')
                else:
                    return render(request, 'Hospital/doc_notapprove_home.html')
    else:
        return render(request, 'Hospital/home.html')


def about(request):
    """
    This function is for about page of hospital management system
    """
    return render(request, 'Hospital/about.html')
