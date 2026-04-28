from django.urls import path

from backend_apps.users.api.users import UsersAPIView

urlpatterns = [
    path('', UsersAPIView.as_view(), name='users-list'),
    path('/<int:pk>/', UsersAPIView.as_view(), name='users-detail'),
]