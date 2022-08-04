import pytest
from django.urls import reverse

from appointment.models import Appointments, Admit


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
def test_create_appointment_date(client, approve_staff):
    data = {'user': 'Ayushi',
            'staff': approve_staff,
            'date': '',
            'timeslot': '11:00',
            'disease': 'Infection',
            'is_bill_generated': False,

            }
    url = reverse('book-appointments')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_date" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_appointment_disease(client, approve_staff):
    data = {'user': 'Ayushi',
            'staff': approve_staff,
            'date': '2022-07-29',
            'timeslot': '11:00',
            'disease': '',
            'is_bill_generated': False,

            }
    url = reverse('book-appointments')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_disease" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_appointment_timeslot(client, approve_staff):
    data = {'user': 'Ayushi',
            'staff': approve_staff,
            'date': '2022-07-29',
            'timeslot': '',
            'disease': 'fever',
            'is_bill_generated': False,

            }
    url = reverse('book-appointments')
    response = client.post(url, data=data, format='multipart/form-data')
    assert ' <p id="error_1_id_timeslot" class="invalid-feedback"><strong>This field cannot be blank.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_appointment_fail_date(client, approve_staff):
    data = {'user': 'Ayushi',
            'staff': approve_staff,
            'date': 2022 - 0o7 - 29,
            'timeslot': '11:00',
            'disease': 'Infection',
            'is_bill_generated': False,

            }
    url = reverse('book-appointments')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_date" class="invalid-feedback"><strong>Enter a valid date.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_appointment_delete(client, create_appointment):
    url = reverse('delete-profile', kwargs={'pk': create_appointment.pk})
    response = client.get(url)
    obj = Appointments.objects.get(id=create_appointment.id)
    obj.delete()
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_room_success(client):
    data = {
        'charge': 2000,
        'AC': True,
        'is_ICU': False,
        'room_type': 'Semi-Private'
    }
    url = reverse('room')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_room_fail(client, create_admin):
    data = {
        'charge': 0,
        'AC': True,
        'is_ICU': False,
        'room_type': 'Semi-Private'
    }
    url = reverse('room')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_appointment_success(client):
    url = reverse('view-appointments')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 405


@pytest.mark.django_db
def test_view_room_success(client):
    url = reverse('view-rooms')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_admit_success(client):
    url = reverse('view-admit-patient')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_timeslot(client):
    url = reverse('search_timeslot')
    response = client.get(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_room(client):
    url = reverse('search_room')
    response = client.get(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_discharge_success(client):
    url = reverse('view-discharge-patient')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_admit(client):
    url = reverse('search_admit')
    response = client.get(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_admit_success(client, approve_staff):
    data = {
        'room': 1,
        'patient': 'Ayushi',
        'staff': approve_staff,
        'disease': 'Infection',
        'in_date': '2022-08-01',
        'is_bill_generated': False,

    }
    url = reverse('admit-patient')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_admit_fail_indate(client, approve_staff):
    data = {
        'room': 0,
        'patient': 'Ayushi',
        'staff': approve_staff,
        'disease': 'Infection',
        'in_date': '',
        'is_bill_generated': False,

    }
    url = reverse('admit-patient')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_in_date" class="invalid-feedback"><strong>This field is required.</strong></p> '
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_admit_fail_room(client, approve_staff):
    data = {
        'room': 0,
        'patient': 'Ayushi',
        'staff': approve_staff,
        'disease': 'Infection',
        'in_date': '2022-08-01',
        'is_bill_generated': False,

    }
    url = reverse('admit-patient')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200
    assert '<p id="error_1_id_room" class="invalid-feedback"><strong>Select a valid choice. That choice is not one of ' \
           'the available choices.</strong></p> ' in str(response.content)


@pytest.mark.django_db
def test_create_admit_fail_patient(client, approve_staff):
    data = {
        'room': 1,
        'patient': '',
        'staff': approve_staff,
        'disease': 'Infection',
        'in_date': '2022-08-01',
        'is_bill_generated': False,

    }
    url = reverse('admit-patient')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200
    assert ' <p id="error_1_id_patient" class="invalid-feedback"><strong>This field is required.</strong></p> ' in str(
        response.content)


@pytest.mark.django_db
def test_create_admit_fail_disease(client, approve_staff):
    data = {
        'room': 1,
        'patient': 'Ayushi',
        'staff': approve_staff,
        'disease': '',
        'in_date': '2022-08-01',
        'is_bill_generated': False,

    }
    url = reverse('admit-patient')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200
    assert '<p id="error_1_id_disease" class="invalid-feedback"><strong>This field is required.</strong></p> </div> ' \
           '</div> <div id=' in str(response.content)


@pytest.mark.django_db
def test_discharge_success(client, create_admit, create_patient):
    print(create_admit)
    data = {
        'patient': create_patient,
        'out_date': '2022-08-02',
        'charge': 2000,

    }
    url = reverse('discharge-patient', kwargs={'pk': create_admit.id})
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 302


@pytest.mark.django_db
def test_discharge_patient_list(client):
    url = reverse('discharge_patient_list')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_discharge_by_doctor(client, create_admit):
    url = reverse('discharge_by_doctor', kwargs={'pk': create_admit.pk})
    response = client.get(url)
    obj = Admit.objects.get(id=create_admit.id)
    obj.save()
    assert response.status_code == 302
