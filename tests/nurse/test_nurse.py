import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_duty_success(client, create_patient, approve_staff):
    data = {
        'staff': approve_staff,
        'patient': create_patient
    }
    url = reverse('duty')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_duty(client):
    url = reverse('view-duty')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 405


@pytest.mark.django_db
def test_search_duty(client):
    url = reverse('search_duty')
    response = client.get(url, format='multipart/form-data')
    assert response.status_code == 200
