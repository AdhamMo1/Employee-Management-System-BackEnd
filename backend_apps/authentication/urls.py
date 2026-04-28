from django.urls import path
from backend_apps.authentication.api.views import login_api

urlpatterns = [
    path('/login', login_api),
]