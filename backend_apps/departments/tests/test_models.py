import pytest
from backend_apps.departments.models import Department


@pytest.mark.django_db
class TestDepartmentModels:

    def test_create_department(self, company):
        department = Department.objects.create(name='Test Department', company=company)
        
        assert department.name == 'Test Department'
        assert department.company.id == company.id
        assert department.created_at is not None

    def test_department_str_method(self, department):
        assert f'Department ID: {department.id} - Department Name: {department.name}' == str(department)

    def test_department_company_relation(self, department, company):
        assert department.company.name == company.name

    def test_department_ordering(self, company):
        dept1 = Department.objects.create(name='First Dept', company=company)
        dept2 = Department.objects.create(name='Second Dept', company=company)
        departments = list(Department.objects.all())
        
        assert departments[0].updated_at >= departments[1].updated_at
