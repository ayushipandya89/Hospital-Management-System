import pytest
from django.contrib.auth import get_user_model

from users.models import CustomUser, UserRole, Staff


@pytest.fixture
def create_doctor_role(client):
    client = UserRole.objects.create(role='Doctor')
    return client


@pytest.fixture
def create_patient_role(client):
    client = UserRole.objects.create(role='Patient')
    return client.id


@pytest.fixture
def create_Nurse_role(client):
    client = UserRole.objects.create(role='Nurse')
    return client


@pytest.fixture
def create_admin_role(client):
    client = UserRole.objects.create(role='admin')
    return client


@pytest.fixture
def create_user(db):
    user = CustomUser.objects.create_user(
        username="Ayushi",
        email="ayushipandya8901@gmail.com",
        phone="+919316789234",
        age=22,
        address='Naroda',
        gender='F',
        role=UserRole.objects.create(role='Patient'),
        password="Qwertyuioop@0987",
        profile='default.jpg',
    )
    return user


# @pytest.fixture
# def important_value():
#     important = True
#     return important


@pytest.fixture
def create_staff(db):
    user = CustomUser.objects.create_user(
        username="Falguni",
        email="falguni12@gmail.com",
        phone="+918926789234",
        age=45,
        address='Ahmedabad',
        gender='F',
        role=UserRole.objects.create(role='Doctor'),
        password="Qwertyuioop@0987",
        profile='default.jpg',
    )
    return user


@pytest.fixture
def approve_staff(db, create_staff):
    staff = Staff.objects.update_or_create(staff_id=create_staff.id, salary=20000, is_approve=True,
                                           is_available=True)
    print('approve_staff:', staff[0])
    return staff


@pytest.fixture
def user_data():
    return {'username': 'Ayushi', 'password': 'Qwertyuioop@0987'}


#
#
# @pytest.fixture
# def create_test_user(user_data):
#     user_model = get_user_model()
#     test_user = user_model.objects.create_user(**user_data)
#     test_user.set_password(user_data.get('password'))
#     return test_user


@pytest.fixture
def authenticated_user(client, user_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.login(**user_data)
    return test_user
