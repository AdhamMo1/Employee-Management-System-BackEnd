import pytest
from backend_apps.departments.models import Department


@pytest.mark.django_db
class TestDepartmentsAPI:

    def test_list_departments_success(self, auth_client, department):
        url = '/api/v1/departments'
        response = auth_client.get(url)
        
        assert response.status_code == 200
        assert 'details' in response.data
        assert 'data' in response.data
        assert 'list_items' in response.data['data']

    def test_list_departments_filtered_by_company(self, auth_client, company, department):
        url = f'/api/v1/departments?company_id={company.id}'
        response = auth_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data['data']['list_items']) > 0

    def test_create_department_success(self, auth_client, company):
        url = '/api/v1/departments'
        data = {
            'request_data': {
                'name': 'New Department',
                'company_id': company.id
            }
        }
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 201
        assert response.data['data']['object_info']['name'] == 'New Department'
        assert Department.objects.filter(name='New Department').exists()

    def test_create_department_duplicate_name(self, auth_client, company, department):
        url = '/api/v1/departments'
        data = {
            'request_data': {
                'name': department.name,
                'company_id': company.id
            }
        }
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 400

    def test_create_department_missing_name(self, auth_client, company):
        url = '/api/v1/departments'
        data = {'request_data': {'company_id': company.id}}
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 400

    def test_create_department_missing_company(self, auth_client):
        url = '/api/v1/departments'
        data = {'request_data': {'name': 'Orphan Department'}}
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 400

    def test_get_department_success(self, auth_client, department):
        url = f'/api/v1/departments/{department.id}/'
        response = auth_client.get(url)
        
        assert response.status_code == 200
        assert response.data['data']['object_info']['id'] == department.id
        assert response.data['data']['object_info']['name'] == department.name

    def test_get_department_not_found(self, auth_client):
        url = '/api/v1/departments/99999/'
        response = auth_client.get(url)
        
        assert response.status_code == 404

    def test_update_department_success(self, auth_client, department):
        url = f'/api/v1/departments/{department.id}/'
        data = {'request_data': {'name': 'Updated Department Name'}}
        response = auth_client.put(url, data, format='json')
        
        assert response.status_code == 200
        assert response.data['data']['object_info']['name'] == 'Updated Department Name'
        department.refresh_from_db()
        assert department.name == 'Updated Department Name'

    def test_update_department_status_success(self, auth_client, department):
        # Department model doesn't have is_active field, so we just test updating name via PUT
        url = f'/api/v1/departments/{department.id}/'
        data = {'request_data': {'name': 'Updated Status Name'}}
        response = auth_client.put(url, data, format='json')

        assert response.status_code == 200
        department.refresh_from_db()
        assert department.name == 'Updated Status Name'

    def test_delete_department_success(self, auth_client, department):
        url = f'/api/v1/departments/{department.id}/'
        response = auth_client.delete(url)
        
        assert response.status_code == 200
        assert not Department.objects.filter(id=department.id).exists()

    def test_hr_can_manage_departments(self, hr_auth_client, company):
        url = '/api/v1/departments'
        data = {
            'request_data': {
                'name': 'HR Created Dept',
                'company_id': company.id
            }
        }
        response = hr_auth_client.post(url, data, format='json')
        
        assert response.status_code == 201

    def test_hr_can_list_departments(self, hr_auth_client, department):
        url = '/api/v1/departments'
        response = hr_auth_client.get(url)
        
        assert response.status_code == 200
