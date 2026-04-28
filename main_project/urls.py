"""
URL configuration for main_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from backend_apps.authentication import urls as auth_urls
from backend_apps.companies import urls as urls_companies
from backend_apps.departments import urls as urls_departments
from backend_apps.employees import urls as urls_employees
from backend_apps.users import urls as urls_users
from main_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/auth', include(auth_urls)),
    path('api/v1/companies', include(urls_companies)),
    path('api/v1/departments', include(urls_departments)),
    path('api/v1/employees', include(urls_employees)),
    path('api/v1/users', include(urls_users)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
