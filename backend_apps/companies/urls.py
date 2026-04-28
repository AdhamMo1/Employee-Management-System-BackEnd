from django.urls import path

from .api.companies import CompaniesAPIView
from .api.dashboard import DashboardAPIView

urlpatterns = [
    path("/<int:pk>/", CompaniesAPIView.as_view(), name='companies-detail'),
    path("", CompaniesAPIView.as_view(), name='companies-list'),
    path("/dashboard", DashboardAPIView.as_view(), name='dashboard'),
]