import pytest

from users.models import CustomUser, UserRole


@pytest.fixture
def create_doctor_role(client):
    client = UserRole.objects.create(role='Doctor')
    print(client.id)
    return client


@pytest.fixture
def create_patient_role(client):
    client = UserRole.objects.create(role='Patient')
    print(client.id)
    return client.id


@pytest.fixture
def create_Nurse_role(client):
    client = UserRole.objects.create(role='Nurse')
    print(client.id)
    return client


@pytest.fixture
def create_admin_role(client):
    client = UserRole.objects.create(role='admin')
    print(client.id)
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

