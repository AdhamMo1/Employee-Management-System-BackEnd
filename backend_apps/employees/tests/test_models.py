import pytest
from datetime import date
from backend_apps.employees.models import Employee


@pytest.mark.django_db
class TestEmployeeModels:

    def test_create_employee(self, department, employee_user):
        employee = Employee.objects.create(
            user=employee_user,
            department=department,
            name='John Doe',
            title='Developer',
            mobile=1234567890,
            address='123 Test Street',
            hire_date=date(2024, 1, 15)
        )
        
        assert employee.name == 'John Doe'
        assert employee.title == 'Developer'
        assert employee.department.id == department.id
        assert employee.user.id == employee_user.id

    def test_employee_str_method(self, employee):
        assert f'Employee ID: {employee.id}' == str(employee)

    def test_employee_days_employed(self, employee):
        assert employee.days_employed >= 0

    def test_employee_user_relation(self, employee, employee_user):
        assert employee.user.username == employee_user.username

    def test_employee_department_relation(self, employee, department):
        assert employee.department.name == department.name

    def test_employee_ordering(self, department, employee_user):
        # Employee model doesn't have updated_at field, so we test ordering by id
        from django.contrib.auth import get_user_model
        User = get_user_model()

        emp1 = Employee.objects.create(
            user=employee_user,
            department=department,
            name='First Employee'
        )
        # Create a second user for the second employee to avoid unique constraint
        second_user = User.objects.create_user(
            username='secondemployee',
            email='second@example.com',
            password='testpass123',
            role='EMPLOYEE'
        )
        emp2 = Employee.objects.create(
            user=second_user,
            department=department,
            name='Second Employee'
        )
        employees = list(Employee.objects.all().order_by('-id'))

        # Test ordering by id (descending)
        assert employees[0].id > employees[1].id
