from django.urls import path

from backend_apps.departments.api.departments import DepartmentsAPIView

urlpatterns = [
    path('', DepartmentsAPIView.as_view(), name='departments-list'),
    path('/<int:pk>/', DepartmentsAPIView.as_view(), name='departments-detail'),
]