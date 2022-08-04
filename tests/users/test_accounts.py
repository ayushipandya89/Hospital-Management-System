import pytest
from django import urls
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from users.models import CustomUser, Staff, Medicine, Bill


@pytest.mark.django_db
class TestHome:

    @pytest.mark.parametrize('param', [
        'Hospital-home',
        'Hospital-about'
    ])
    def test_render_views(self, client, param, create_admin_role):
        data = {
            'username': 'Ayushi',
            'password': 'Qwertyuioop@0987',
            "role": create_admin_role.id,
        }
        temp_url = urls.reverse(param)
        resp = client.post(temp_url, data=data)
        assert resp.status_code == 200


@pytest.mark.django_db
def test_create_user_success(client, create_admin_role):
    data = {
        "username": "admin",
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
def test_create_user_fail_username(client, create_admin_role):
    data = {
        "username": "",
        'email': "ayushi.inexture@gmail.com",
        'phone': "+918967342221",
        'age': 24,
        "address": 'Ahmedabad',
        "gender": 'M',
        "role": create_admin_role.id,
        "password1": "qwertyuioop@0987",
        "password2": 'qwertyuioop@0987',
        "profile": 'default.jpg',

    }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assertTemplateUsed(response, 'users/register.html')
    assert '<p id="error_1_id_username" class="invalid-feedback"><strong>This field is required.</strong>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_fail_email(client, create_admin_role):
    data = {
        "username": "admin",
        'email': "",
        'phone': "+918967342221",
        'age': 24,
        "address": 'Ahmedabad',
        "gender": 'M',
        "role": create_admin_role.id,
        "password1": "qwertyuioop@0987",
        "password2": 'qwertyuioop@0987',
        "profile": 'default.jpg',

    }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assertTemplateUsed(response, 'users/register.html')
    assert '<p id="error_1_id_email" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_fail_phone(client, create_admin_role):
    data = {
        "username": "admin",
        'email': "ayushi.inexture@gmail.com",
        'phone': "",
        'age': 24,
        "address": 'Ahmedabad',
        "gender": 'M',
        "role": create_admin_role.id,
        "password1": "qwertyuioop@0987",
        "password2": 'qwertyuioop@0987',
        "profile": 'default.jpg',

    }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assertTemplateUsed(response, 'users/register.html')
    assert '<p id="error_1_id_phone" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_fail_age(client, create_admin_role):
    data = {
        "username": "admin",
        'email': "ayushi.inexture@gmail.com",
        'phone': "+918967342221",
        'age': 0,
        "address": 'Ahmedabad',
        "gender": 'M',
        "role": create_admin_role.id,
        "password1": "qwertyuioop@0987",
        "password2": 'qwertyuioop@0987',
        "profile": 'default.jpg',

    }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assertTemplateUsed(response, 'users/register.html')
    assert '<p id="error_1_id_age" class="invalid-feedback"><strong>Please enter age above 21</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_fail_address(client, create_admin_role):
    data = {
        "username": "admin",
        'email': "ayushi.inexture@gmail.com",
        'phone': "+918967342221",
        'age': 24,
        "address": '',
        "gender": 'M',
        "role": create_admin_role.id,
        "password1": "qwertyuioop@0987",
        "password2": 'qwertyuioop@0987',
        "profile": 'default.jpg',
    }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assertTemplateUsed(response, 'users/register.html')
    assert '<p id="error_1_id_address" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_fail_gender(client, create_admin_role):
    data = {
        "username": "admin",
        'email': "ayushi.inexture@gmail.com",
        'phone': "+918967342221",
        'age': 24,
        "address": 'Ahmedabad',
        "gender": '',
        "role": create_admin_role.id,
        "password1": "qwertyuioop@0987",
        "password2": 'qwertyuioop@0987',
        "profile": 'default.jpg',
    }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assertTemplateUsed(response, 'users/register.html')
    assert '<p id="error_1_id_gender" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_fail_password1(client, create_admin_role):
    data = {
        "username": "admin",
        'email': "ayushi.inexture@gmail.com",
        'phone': "+918967342221",
        'age': 24,
        "address": 'Ahmedabad',
        "gender": 'M',
        "role": create_admin_role.id,
        "password1": "",
        "password2": 'qwertyuioop@0987',
        "profile": 'default.jpg',
    }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assertTemplateUsed(response, 'users/register.html')
    assert '<p id="error_1_id_password1" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_fail_password2(client, create_admin_role):
    data = {
        "username": "admin",
        'email': "ayushi.inexture@gmail.com",
        'phone': "+918967342221",
        'age': 24,
        "address": 'Ahmedabad',
        "gender": 'M',
        "role": create_admin_role.id,
        "password1": "qwertyuioop@0987",
        "password2": '',
        "profile": 'default.jpg',
    }
    url = reverse('register')
    response = client.post(url, data=data, format='multipart/form-data')
    assertTemplateUsed(response, 'users/register.html')
    assert '<p id="error_1_id_password2" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_success(client):
    data = {
        'username': 'Ayushi',
        'password': 'Qwertyuioop@0987'
    }
    url = reverse('login')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_fail(client):
    data = {
        'username': 'abc',
        'password': 'abc@123',
    }
    url = reverse('login')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_fail_username(client, create_user):
    a = CustomUser.objects.filter(username='abc').exists()
    assert a == False


@pytest.mark.django_db
def test_login_fail_password(client, create_user):
    a = CustomUser.objects.filter(username=create_user).filter(password='abcd').exists()
    assert a == False


@pytest.mark.django_db
def test_user_logout(client, authenticated_user):
    url = urls.reverse('logout')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_update_username(client, create_user):
    url = reverse('update-profile', kwargs={'pk': create_user.pk})
    response = client.get(url)
    obj = CustomUser.objects.get(username=create_user)
    obj.username = 'Dipak'
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_update_email(client, create_user):
    url = reverse('update-profile', kwargs={'pk': create_user.pk})
    response = client.get(url)
    obj = CustomUser.objects.get(username=create_user)
    obj.email = 'dipak12@gmail.com'
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_update_phone(client, create_user):
    url = reverse('update-profile', kwargs={'pk': create_user.pk})
    response = client.get(url)
    obj = CustomUser.objects.get(username=create_user)
    obj.phone = '+917835421356'
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_update_age(client, create_user):
    url = reverse('update-profile', kwargs={'pk': create_user.pk})
    response = client.get(url)
    obj = CustomUser.objects.get(username=create_user)
    obj.age = 45
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_update_address(client, create_user):
    url = reverse('update-profile', kwargs={'pk': create_user.pk})
    response = client.get(url)
    obj = CustomUser.objects.get(username=create_user)
    obj.address = 'India'
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_delete(client, create_user):
    url = reverse('delete-profile', kwargs={'pk': create_user.pk})
    response = client.get(url)
    obj = CustomUser.objects.get(username=create_user)
    obj.delete()
    assert response.status_code == 200


@pytest.mark.django_db
def test_staff_update_speciality(client, approve_staff, create_speciality):
    url = reverse('update-staff-profile', kwargs={'pk': approve_staff[0].pk})
    response = client.get(url)
    obj = Staff.objects.get(staff__username=approve_staff[0])
    obj.speciality = create_speciality
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_staff_update_is_available(client, approve_staff):
    url = reverse('update-staff-profile', kwargs={'pk': approve_staff[0].pk})
    response = client.get(url)
    obj = Staff.objects.get(staff__username=approve_staff[0])
    obj.is_available = True
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_staff_update_is_approve(client, approve_staff):
    url = reverse('update-staff-profile', kwargs={'pk': approve_staff[0].pk})
    response = client.get(url)
    obj = Staff.objects.get(staff__username=approve_staff[0])
    obj.is_approve = True
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_staff_update_salary(client, approve_staff):
    url = reverse('update-staff-profile', kwargs={'pk': approve_staff[0].pk})
    response = client.get(url)
    obj = Staff.objects.get(staff__username=approve_staff[0])
    obj.salary = 50000
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_role_success(client):
    data = {
        'role': 'Patient',
    }
    url = reverse('add_role')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_role_fail(client, login_check):
    data = {
        'role': '',
    }
    url = reverse('add_role')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_role" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_speciality_success(client):
    data = {
        'speciality': 'Patient',
    }
    url = reverse('add_speciality')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_speciality_fail(client):
    data = {
        'speciality': '',
    }
    url = reverse('add_speciality')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_speciality" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_password_reset(client):
    url = reverse('password_reset')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_user_success(client):
    url = reverse('view-user')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_staff_success(client):
    url = reverse('view-staff')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_emergency_success(client):
    url = reverse('view-emergency')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_prescription_success(client):
    url = reverse('view-prescription')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_feedback_success(client):
    url = reverse('view-feedback')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_today_appointment(client):
    url = reverse('view_todays_appointment')
    response = client.post(url, format='multipart/form-data')
    assert response.status_code == 405


@pytest.mark.django_db
def test_emergency_success(client, create_user):
    data = {
        'patient': create_user,
        'staff': 'admin',
        'datetime': '2022-08-01',
        'disease': 'fever',
        'charge': 2000,
        'is_bill_generated': False
    }
    url = reverse('emergency')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_emergency_fail_patinet(client, create_user):
    data = {
        'patient': '',
        'staff': 'admin',
        'datetime': '2022-08-01',
        'disease': 'fever',
        'charge': 2000,
        'is_bill_generated': False
    }
    url = reverse('emergency')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_patient" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_emergency_fail_staff(client, create_user):
    data = {
        'patient': create_user,
        'staff': '',
        'datetime': '2022-08-01',
        'disease': 'fever',
        'charge': 2000,
        'is_bill_generated': False
    }
    url = reverse('emergency')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_staff" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_emergency_fail_datetime(client, create_user):
    data = {
        'patient': create_user,
        'staff': 'admin',
        'datetime': '',
        'disease': 'fever',
        'charge': 2000,
        'is_bill_generated': False
    }
    url = reverse('emergency')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_datetime" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_emergency_fail_disease(client, create_user):
    data = {
        'patient': create_user,
        'staff': 'admin',
        'datetime': '2022-08-01',
        'disease': '',
        'charge': 2000,
        'is_bill_generated': False
    }
    url = reverse('emergency')
    response = client.post(url, data=data, format='multipart/form-data')
    assert '<p id="error_1_id_disease" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_medicine_success(client, create_user):
    data = {
        'medicine_name': 'Dolo',
        'charge': 12.78,

    }
    url = reverse('add-medicine')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 302


@pytest.mark.django_db
def test_medicine_fail(client, create_user):
    data = {
        'medicine_name': '',
        'charge': 0,

    }
    url = reverse('add-medicine')
    response = client.post(url, data=data, format='multipart/form-data')
    # print(str(response.content))
    assert '<p id="error_1_id_medicine_name" class="invalid-feedback"><strong>This field is required.</strong></p> ' in str(
        response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_medicine_name(client, create_medicine):
    url = reverse('update-medicine', kwargs={'pk': create_medicine.pk})
    response = client.get(url)
    obj = Medicine.objects.get(medicine_name=create_medicine.medicine_name)
    obj.medicine_name = 'Peracitamol'
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_medicine_charge(client, create_medicine):
    url = reverse('update-medicine', kwargs={'pk': create_medicine.pk})
    response = client.get(url)
    obj = Medicine.objects.get(medicine_name=create_medicine.medicine_name)
    obj.charge = 23.1
    obj.save()
    assert response.status_code == 200


@pytest.mark.django_db
def test_bill_success(client, create_user):
    data = {
        'patient': create_user,
        'staff_charge': 2000,
        'other_charge': 0,
        'is_paid': False
    }
    url = reverse('create-bill')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200


@pytest.mark.django_db
def test_bill_fail_patient(client, create_user):
    data = {
        'patient': '',
        'staff_charge': 2000,
        'other_charge': 0,
        'is_paid': False
    }
    url = reverse('create-bill')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 200
    assert '<p id="error_1_id_patient" class="invalid-feedback"><strong>This field is required.</strong></p>' in str(
        response.content)

