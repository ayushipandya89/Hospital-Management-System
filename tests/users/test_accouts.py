import pytest
from django import urls
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from tests.conftest import create_user
from users.models import CustomUser


@pytest.mark.django_db
class TestHome:

    @pytest.mark.parametrize('param', [
        'Hospital-home',
        'Hospital-about'
    ])
    def test_render_views(self, client, param):
        temp_url = urls.reverse(param)
        resp = client.get(temp_url)
        assert resp.status_code == 200


@pytest.mark.django_db
def test_create_user_success(client, create_admin_role):
    data = {"username": "admin",
            'email': "ayushi.inexture@gmail.com",
            'phone': "+918967342221",
            'age': 24,
            "address": 'Ahmedabad',
            "gender": 'M',
            "role": create_admin_role.id,
            "password1": "qwertyuioop@0987",
            "password2": 'qwertyuioop@0987',
            "profile": 'default.jpg',
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
            }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_user_fail(client, create_admin_role):
    data = {
        "username": "",
        'email': "",
        'phone': "",
        "age": 0,
        "address": '',
        "gender": '',
        "role_id": '',
        "password1": '',
        "password2": '',
        "profile": '',
    }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assertTemplateUsed(response, 'users/register.html')
    assert '<p id="error_1_id_username" class="invalid-feedback"><strong>This field is required.</strong>' in str(
        response.content)
    assert '<p id="error_1_id_email" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert '<p id="error_1_id_phone" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert '<p id="error_1_id_age" class="invalid-feedback"><strong>Please enter age above 21</strong></p>' in str(
        response.content)
    assert '<p id="error_1_id_address" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert '<p id="error_1_id_gender" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert '<p id="error_1_id_password1" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert '<p id="error_1_id_password2" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_success(client, create_user):
    a = CustomUser.objects.filter(username=create_user).exists()
    assert a


@pytest.mark.django_db
def test_login_fail_username(client, create_user):
    a = CustomUser.objects.filter(username='abc').exists()
    assert a == False


@pytest.mark.django_db
def test_login_fail_password(client, create_user):
    a = CustomUser.objects.filter(username=create_user).filter(password='abcd').exists()
    assert a == False
