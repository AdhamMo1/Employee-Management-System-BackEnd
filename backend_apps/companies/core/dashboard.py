from rest_framework import status

from backend_apps.companies.models import Company
from backend_apps.companies.shared_utils import message_manager
from backend_apps.departments.models import Department
from backend_apps.employees.models import Employee
from backend_apps.users.models import UserAccounts


class DashboardHandle:
    def __init__(self, request):
        self.request = request
        self.cloud_message = message_manager.message.get("dashboard", {})

        requested_language = self.request.META.get("HTTP_LN", "en")
        self.ln = requested_language if requested_language in message_manager.languages else "en"

        self.company_id = request.GET.get('company_id')

    def get_stats(self):
        # Base querysets
        companies_qs = Company.objects.all()
        departments_qs = Department.objects.all()
        employees_qs = Employee.objects.all()
        users_qs = UserAccounts.objects.all()

        # Filter by company if provided
        if self.company_id:
            try:
                company_id_int = int(self.company_id)
                companies_qs = companies_qs.filter(id=company_id_int)
                departments_qs = departments_qs.filter(company_id=company_id_int)
                employees_qs = employees_qs.filter(department__company_id=company_id_int)
                users_qs = users_qs.filter(company_id=company_id_int)
            except (ValueError, TypeError):
                pass

        # Counts
        total_companies = companies_qs.count()
        total_departments = departments_qs.count()
        total_employees = employees_qs.count()

        # Active/Inactive employees (based on user account status)
        employee_user_ids = list(employees_qs.values_list('user_id', flat=True))
        active_employees = users_qs.filter(id__in=employee_user_ids, is_active=True).count()
        inactive_employees = users_qs.filter(id__in=employee_user_ids, is_active=False).count()

        # Average days employed
        avg_days = 0
        if total_employees > 0:
            total_days = sum(emp.days_employed for emp in employees_qs)
            avg_days = round(total_days / total_employees)

        data = {
            "total_companies": total_companies,
            "total_departments": total_departments,
            "total_employees": total_employees,
            "active_employees": active_employees,
            "inactive_employees": inactive_employees,
            "avg_days_employed": avg_days,
        }

        # Add company filter info if applied
        if self.company_id:
            try:
                company_id_int = int(self.company_id)
                company = Company.objects.filter(id=company_id_int).first()
                if company:
                    data["filtered_by_company"] = {
                        "id": company.id,
                        "name": company.name,
                    }
            except (ValueError, TypeError):
                pass

        success_message = self.cloud_message.get("stats_success", {}).get(self.ln, "Dashboard stats retrieved successfully")
        return status.HTTP_200_OK, success_message, data
