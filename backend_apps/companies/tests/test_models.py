import pytest
from backend_apps.companies.models import Company


@pytest.mark.django_db
class TestCompanyModels:

    def test_create_company(self):
        company = Company.objects.create(name='Test Company', is_active=True)
        
        assert company.name == 'Test Company'
        assert company.is_active is True
        assert company.created_at is not None

    def test_company_str_method(self, company):
        assert f'Company ID: {company.id} - Company Name: {company.name}' == str(company)

    def test_company_ordering(self, company):
        company2 = Company.objects.create(name='Another Company')
        companies = list(Company.objects.all())
        
        assert companies[0].updated_at >= companies[1].updated_at

    def test_company_is_active_default(self):
        company = Company.objects.create(name='Active Company')
        assert company.is_active is True
