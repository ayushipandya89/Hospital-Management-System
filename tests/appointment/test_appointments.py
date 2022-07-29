import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_appointment_success(client, approve_staff):
    data = {'user': 'Ayushi',
            'staff': approve_staff,
            'date': '2022-07-29',
            'timeslot': '11:00',
            'disease': 'Infection',
            'is_bill_generated': False,

            }
    url = reverse('book-appointments')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_appointment_fail(client):
    data = {'user': '',
            'staff': ' ',
            'date': '',
            'timeslot': '',
            'disease': '',
            'is_bill_generated': '',

            }
    url = reverse('book-appointments')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_staff" class="invalid-feedback"><strong>Select a valid choice. That choice is not one ' \
           'of the available choices.</strong></p>' in str(response.content)
    assert '<p id="error_1_id_date" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert '<p id="error_1_id_disease" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert ' <p id="error_1_id_timeslot" class="invalid-feedback"><strong>This field cannot be blank.</strong></p>'
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_appointment_fail_date(client,approve_staff):
    data = {'user': 'Ayushi',
            'staff': approve_staff,
            'date': 2022 - 0o7 - 29,
            'timeslot': '11:00',
            'disease': 'Infection',
            'is_bill_generated': False,

            }
    url = reverse('book-appointments')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_date" class="invalid-feedback"><strong>Enter a valid date.</strong></p>' in str(response.content)
    assert response.status_code == 200


from users.models import Staff
#
#
# def user(create_staff):
#     print("create_staff:", create_staff)
#     assert create_staff
#
#
# def test_if_important(create_staff):
#     assert create_staff.username == 'Falguni'
# #
#
# def test_if_important1(approve_staff):
#     print('approve_staff1:', approve_staff.is_approve)
#     assert approve_staff == True
#
#
# @pytest.mark.django_db
# def test_login_fail_password(client, create_staff):
#     print('create_staff_username:', create_staff.id)
#     a = Staff.objects.filter(staff=create_staff.id).exists()
#     print('a:', a)
#     assert a == False
