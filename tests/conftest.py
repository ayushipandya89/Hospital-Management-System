import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from appointment.models import Appointments, Admit, Room
from users.models import CustomUser, UserRole, Staff, Patient, StaffSpeciality, Medicine, Bill


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


@pytest.fixture
def create_patient(db, create_user):
    staff = Patient.objects.update_or_create(patient_id=create_user.id)
    return staff


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
def create_admin(db):
    user = CustomUser.objects.create_user(
        username="admin",
        email="ayushi.inexture@gmail.com",
        phone="+919316789789",
        age=22,
        address='India',
        gender='F',
        role=UserRole.objects.create(role='admin'),
        password="Qwertyuioop@0987",
        profile='default.jpg',
    )
    # print(user)
    return user


@pytest.fixture
def approve_staff(db, create_staff):
    staff = Staff.objects.update_or_create(staff_id=create_staff.id, salary=20000, is_approve=True,
                                           is_available=True)
    return staff


@pytest.fixture
def create_speciality(db, create_staff):
    staff = StaffSpeciality.objects.create(speciality='MD')
    return staff


@pytest.fixture
def create_medicine(db):
    medicine = Medicine.objects.create(medicine_name='Dolo', charge=12.34)
    return medicine


@pytest.fixture
def create_appointment(db, create_user, approve_staff):
    appointment = Appointments.objects.create(user_id=create_user.id, staff_id=approve_staff[0].id, date='2022-08-05',
                                              timeslot='11:00', disease='infection', is_bill_generated=False)
    return appointment


@pytest.fixture
def create_room(db):
    room = Room.objects.create(charge=2000, AC=True, is_ICU=False, room_type='Semi-Private')
    return room


@pytest.fixture
def create_admit(db, create_user, approve_staff, create_room, create_patient):
    print(create_patient[0].patient.id)
    admit = Admit.objects.create(room_id=create_room.id, patient=create_patient[0],
                                 disease='fever', in_date='2022-08-05')
    print(admit)
    return admit


@pytest.fixture
def user_data():
    return {'username': 'Ayushi', 'password': 'Qwertyuioop@0987'}


@pytest.fixture
def authenticated_user(client, user_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.login(**user_data)
    return test_user


@pytest.fixture()
@pytest.mark.django_db
def login_check(create_admin, client):
    data = {
        'username': 'admin',
        'password': 'Qwertyuioop@0987'
    }
    url = reverse('login')
    response = client.post(url, data=data, format='multipart/form-data')
    assert response.status_code == 302
    user = CustomUser.objects.get(username='admin')
    return user
