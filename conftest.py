import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from backend_apps.companies.models import Company
from backend_apps.departments.models import Department
from backend_apps.employees.models import Employee

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    user = User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='admin123',
        role='SYSTEM_ADMINISTRATOR'
    )
    return user


@pytest.fixture
def hr_user(db):
    user = User.objects.create_user(
        username='hrmanager',
        email='hr@test.com',
        password='hrpass123',
        role='HR_MANAGER'
    )
    return user


@pytest.fixture
def employee_user(db):
    user = User.objects.create_user(
        username='employee',
        email='employee@test.com',
        password='employeepass',
        role='EMPLOYEE'
    )
    return user


@pytest.fixture
def auth_client(api_client, admin_user):
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return api_client


@pytest.fixture
def hr_auth_client(api_client, hr_user):
    refresh = RefreshToken.for_user(hr_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return api_client


@pytest.fixture
def employee_auth_client(api_client, employee_user):
    refresh = RefreshToken.for_user(employee_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return api_client


@pytest.fixture
def company(db):
    return Company.objects.create(name='Test Company', is_active=True)


@pytest.fixture
def department(db, company):
    return Department.objects.create(name='Test Department', company=company)


@pytest.fixture
def employee(db, department, employee_user):
    emp = Employee.objects.create(
        user=employee_user,
        department=department,
        name='John Doe',
        title='Developer',
        mobile=1234567890,
        address='123 Test Street'
    )
    return emp


@pytest.fixture
def request_factory():
    from django.test import RequestFactory
    return RequestFactory()
