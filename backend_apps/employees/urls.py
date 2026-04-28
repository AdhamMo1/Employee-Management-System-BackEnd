from django.urls import path

from backend_apps.employees.api.employees import EmployeesAPIView

urlpatterns = [
    path('', EmployeesAPIView.as_view(), name='employees-list'),
    path('/<int:pk>/', EmployeesAPIView.as_view(), name='employees-detail'),
]