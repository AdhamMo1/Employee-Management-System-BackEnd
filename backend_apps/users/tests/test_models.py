import pytest
from backend_apps.users.models import UserAccounts


@pytest.mark.django_db
class TestUserModels:

    def test_create_user(self):
        user = UserAccounts.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='EMPLOYEE'
        )
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'EMPLOYEE'
        assert user.check_password('testpass123')
        assert user.is_active is True

    def test_create_superuser(self):
        admin = UserAccounts.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='SYSTEM_ADMINISTRATOR'
        )
        
        assert admin.is_superuser is True
        assert admin.is_staff is True
        assert admin.role == 'SYSTEM_ADMINISTRATOR'

    def test_user_str_method(self, admin_user):
        status = "Active" if admin_user.is_active else "Inactive"
        expected = f"User account {admin_user.first_name} ID: {admin_user.id}  Email: {admin_user.email} ({admin_user.role}) - {status}"
        assert str(admin_user) == expected

    def test_user_roles(self, admin_user, hr_user, employee_user):
        assert admin_user.role == 'SYSTEM_ADMINISTRATOR'
        assert hr_user.role == 'HR_MANAGER'
        assert employee_user.role == 'EMPLOYEE'

    def test_user_company_relation(self, employee_user, company):
        employee_user.company = company
        employee_user.save()
        
        assert employee_user.company.id == company.id
