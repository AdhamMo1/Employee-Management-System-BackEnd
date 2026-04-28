import pytest
from backend_apps.employees.models import Employee


@pytest.mark.django_db
class TestEmployeesAPI:

    def test_list_employees_success(self, auth_client, employee):
        url = '/api/v1/employees'
        response = auth_client.get(url)
        
        assert response.status_code == 200
        assert 'details' in response.data
        assert 'data' in response.data
        assert 'list_items' in response.data['data']

    def test_list_employees_filtered_by_company(self, auth_client, employee, company):
        # The implementation filters by user__company_id, so we need to assign the company to the employee's user
        employee.user.company = company
        employee.user.save()
        url = f'/api/v1/employees?company_id={company.id}'
        response = auth_client.get(url)

        assert response.status_code == 200
        assert len(response.data['data']['list_items']) > 0

    def test_create_employee_success(self, auth_client, department, company):
        url = '/api/v1/employees'
        data = {
            'request_data': {
                'name': 'New Employee',
                'email': 'newemployee@test.com',
                'password': 'employeepass123',
                'department_id': department.id,
                'company_id': company.id,
                'title': 'Developer',
                'mobile': 1234567890,
                'address': '123 Test St'
            }
        }
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 200
        assert response.data['data']['object_info']['name'] == 'New Employee'
        assert Employee.objects.filter(name='New Employee').exists()

    def test_create_employee_missing_name(self, auth_client, department, company):
        url = '/api/v1/employees'
        data = {
            'request_data': {
                'password': 'password123',
                'department_id': department.id,
                'company_id': company.id
            }
        }
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 400

    def test_create_employee_missing_email(self, auth_client, department, company):
        url = '/api/v1/employees'
        data = {
            'request_data': {
                'password': 'password123',
                'department_id': department.id,
                'company_id': company.id
            }
        }
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 400

    def test_get_employee_success(self, auth_client, employee):
        url = f'/api/v1/employees/{employee.id}/'
        response = auth_client.get(url)
        
        assert response.status_code == 200
        assert response.data['data']['object_info']['id'] == employee.id
        assert response.data['data']['object_info']['name'] == employee.name

    def test_get_employee_not_found(self, auth_client):
        url = '/api/v1/employees/99999/'
        response = auth_client.get(url)
        
        assert response.status_code == 404

    def test_update_employee_success(self, auth_client, employee):
        url = f'/api/v1/employees/{employee.id}/'
        data = {'request_data': {'name': 'Updated Employee Name'}}
        response = auth_client.put(url, data, format='json')
        
        assert response.status_code == 200
        assert response.data['data']['object_info']['name'] == 'Updated Employee Name'
        employee.refresh_from_db()
        assert employee.name == 'Updated Employee Name'

    def test_update_employee_status_success(self, auth_client, employee):
        url = f'/api/v1/employees/{employee.id}/'
        data = {'request_data': {'is_active': False}}
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == 200

    def test_delete_employee_success(self, auth_client, employee):
        url = f'/api/v1/employees/{employee.id}/'
        response = auth_client.delete(url)
        
        assert response.status_code == 200
        assert not Employee.objects.filter(id=employee.id).exists()

    def test_hr_can_manage_employees(self, hr_auth_client, department, company):
        url = '/api/v1/employees'
        data = {
            'request_data': {
                'name': 'HR Created Employee',
                'email': 'hrcreated@test.com',
                'password': 'password123',
                'department_id': department.id,
                'company_id': company.id,
                'title': 'Analyst'
            }
        }
        response = hr_auth_client.post(url, data, format='json')
        
        assert response.status_code == 200

    def test_hr_can_list_employees(self, hr_auth_client, employee):
        url = '/api/v1/employees'
        response = hr_auth_client.get(url)
        
        assert response.status_code == 200

    def test_employee_cannot_create_employees(self, employee_auth_client, department, company):
        url = '/api/v1/employees'
        data = {
            'request_data': {
                'name': 'Unauthorized Employee',
                'email': 'unauthorized@test.com',
                'password': 'password123',
                'department_id': department.id,
                'company_id': company.id,
                'title': 'Tester'
            }
        }
        response = employee_auth_client.post(url, data, format='json')
        
        assert response.status_code == 403
