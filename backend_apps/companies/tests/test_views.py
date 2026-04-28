import pytest
from backend_apps.companies.models import Company
from backend_apps.departments.models import Department
from backend_apps.employees.models import Employee


@pytest.mark.django_db
class TestCompaniesAPI:

    def test_list_companies_success(self, auth_client, company):
        url = '/api/v1/companies'
        response = auth_client.get(url)
        
        assert response.status_code == 200
        assert 'details' in response.data
        assert 'data' in response.data
        assert 'list_items' in response.data['data']

    def test_list_companies_unauthorized(self, api_client):
        url = '/api/v1/companies'
        response = api_client.get(url)
        
        assert response.status_code == 401

    def test_create_company_success(self, auth_client):
        url = '/api/v1/companies'
        data = {'request_data': {'name': 'New Test Company'}}
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 201
        assert response.data['data']['object_info']['name'] == 'New Test Company'
        assert Company.objects.filter(name='New Test Company').exists()

    def test_create_company_duplicate_name(self, auth_client, company):
        url = '/api/v1/companies'
        data = {'request_data': {'name': company.name}}
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 400

    def test_create_company_missing_name(self, auth_client):
        url = '/api/v1/companies'
        data = {'request_data': {}}
        response = auth_client.post(url, data, format='json')
        
        assert response.status_code == 400

    def test_get_company_success(self, auth_client, company):
        url = f'/api/v1/companies/{company.id}/'
        response = auth_client.get(url)
        
        assert response.status_code == 200
        assert response.data['data']['object_info']['id'] == company.id
        assert response.data['data']['object_info']['name'] == company.name

    def test_get_company_not_found(self, auth_client):
        url = '/api/v1/companies/99999/'
        response = auth_client.get(url)
        
        assert response.status_code == 404

    def test_update_company_success(self, auth_client, company):
        url = f'/api/v1/companies/{company.id}/'
        data = {'request_data': {'name': 'Updated Company Name'}}
        response = auth_client.put(url, data, format='json')
        
        assert response.status_code == 200
        assert response.data['data']['object_info']['name'] == 'Updated Company Name'
        company.refresh_from_db()
        assert company.name == 'Updated Company Name'

    def test_update_company_status_success(self, auth_client, company):
        url = f'/api/v1/companies/{company.id}/'
        data = {'request_data': {'is_active': False}}
        response = auth_client.patch(url, data, format='json')
        
        assert response.status_code == 200
        company.refresh_from_db()
        assert company.is_active is False

    def test_delete_company_success(self, auth_client, company):
        url = f'/api/v1/companies/{company.id}/'
        response = auth_client.delete(url)
        
        assert response.status_code == 200
        assert not Company.objects.filter(id=company.id).exists()

    def test_hr_can_list_companies(self, hr_auth_client, company):
        url = '/api/v1/companies'
        response = hr_auth_client.get(url)
        
        assert response.status_code == 200


@pytest.mark.django_db
class TestDashboardAPI:

    def test_dashboard_stats_success(self, auth_client, company, department, employee):
        url = '/api/v1/companies/dashboard'
        response = auth_client.get(url)
        
        assert response.status_code == 200
        assert 'details' in response.data
        assert 'data' in response.data
        data = response.data['data']
        assert 'total_companies' in data
        assert 'total_departments' in data
        assert 'total_employees' in data
        assert 'active_employees' in data
        assert 'inactive_employees' in data

    def test_dashboard_stats_filtered_by_company(self, auth_client, company):
        url = f'/api/v1/companies/dashboard?company_id={company.id}'
        response = auth_client.get(url)
        
        assert response.status_code == 200
        assert 'filtered_by_company' in response.data['data']
        assert response.data['data']['filtered_by_company']['id'] == company.id

    def test_dashboard_unauthorized(self, api_client):
        url = '/api/v1/companies/dashboard'
        response = api_client.get(url)
        
        assert response.status_code == 401

    def test_dashboard_hr_access(self, hr_auth_client, company):
        url = '/api/v1/companies/dashboard'
        response = hr_auth_client.get(url)
        
        assert response.status_code == 200
