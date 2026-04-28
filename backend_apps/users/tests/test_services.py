import pytest
from backend_apps.users.core.users import UserHandle


@pytest.mark.django_db
class TestUserServices:

    def test_user_handle_view(self, request_factory, admin_user):
        request = request_factory.get('/api/v1/users')
        request.user = admin_user
        request.META = {'HTTP_LN': 'en'}
        
        handle = UserHandle(request)
        status_code, message, data = handle.view(admin_user.id)
        
        assert status_code == 200
        assert data['object_info']['id'] == admin_user.id

    def test_user_handle_all(self, request_factory, admin_user, hr_user):
        request = request_factory.get('/api/v1/users')
        request.user = admin_user
        request.META = {'HTTP_LN': 'en'}
        
        handle = UserHandle(request)
        status_code, message, data = handle.all()
        
        assert status_code == 200
        assert 'list_items' in data

    def test_user_handle_create_validation(self, request_factory, admin_user):
        request = request_factory.post('/api/v1/users', {}, content_type='application/json')
        request.user = admin_user
        request.META = {'HTTP_LN': 'en'}
        
        handle = UserHandle(request)
        status_code, message, data = handle.create()
        
        assert status_code == 400
