import json
import re

from rest_framework import status
from django.db import transaction

from backend_apps.employees.models import Employee
from backend_apps.employees.shared_utils import message_manager
from backend_apps.users.models import RoleChoices


class EmployeeHandle:
    def __init__(self, request):
        self.request = request
        self.error_handling = []
        self.cloud_message = message_manager.message.get("employees", {})

        requested_language = self.request.META.get("HTTP_LN", "en")
        self.ln = requested_language if requested_language in message_manager.languages else "en"

        self.modelDB = Employee.objects.all()
        try:
            self.request_data = json.loads(request.body).get('request_data', {})
        except:
            self.request_data = {}

    def view(self, pk=None, model_object=None):
        object_info = None

        if model_object is None:
            try:
                model_object = self.modelDB.get(id=pk)
            except:
                model_object = None

        if model_object:
            object_info = {
                "id": model_object.id,
                "name": model_object.name,
                "email": model_object.user.email if model_object.user else None,
                "title": model_object.title,
                "department_id": model_object.department.id if model_object.department else None,
                "department_name": model_object.department.name if model_object.department else None,
                "company_id": model_object.department.company.id if model_object.department and model_object.department.company else None,
                "company_name": model_object.department.company.name if model_object.department and model_object.department.company else None,
                "hire_date": model_object.hire_date,
                "mobile": model_object.mobile,
                "address": model_object.address,
                "days_employed": model_object.days_employed,
                "is_active": model_object.user.is_active,
            }
        else:
            return status.HTTP_404_NOT_FOUND, self.cloud_message.get("not_found", {}).get(self.ln, "Not found!"), None

        success_message = self.cloud_message.get("view_success", {}).get(self.ln, "Employee retrieved successfully")
        return status.HTTP_200_OK, success_message, {
            "object_info": object_info
        }

    def all(self):
        from django.core.paginator import Paginator

        response_data = {
            "list_items": [],
            "total_items": 0,
            "page": self.request.GET.get("page", 1),
            "total_pages": 0
        }

        queryset = self.modelDB.order_by('-id')

        if self.request.GET.get("company_id"):
            queryset = queryset.filter(user__company_id=self.request.GET.get("company_id"))

        if self.request.GET.get("department_id"):
            queryset = queryset.filter(department_id=self.request.GET.get("department_id"))

        try:
            per_page = int(self.request.GET.get("per_page", 10))
        except:
            per_page = 10

        items = Paginator(queryset, per_page)

        try:
            all_items = items.page(self.request.GET.get("page", 1))
            response_data["total_pages"] = items.num_pages
            response_data["total_items"] = queryset.count()
        except:
            all_items = []

        for model_object in all_items:
            response_data["list_items"].append(self.view(model_object=model_object)[2]["object_info"])

        success_message = self.cloud_message.get("all_success", {}).get(self.ln, "Employees retrieved successfully")
        return status.HTTP_200_OK, success_message, response_data

    def check_name(self):
        fun_message = self.cloud_message.get("check_name", {})

        name = self.request_data.get("name", "").strip()

        if not name:
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("required", {}).get(self.ln, "Employee name is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if len(name) < 2:
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("min_length", {}).get(self.ln, "Employee name must be at least 2 characters long"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if len(name) > 255:
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("max_length", {}).get(self.ln, "Employee name must not exceed 255 characters"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if not re.match(r'^[\w\s\-\.&]+$', name):
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("invalid_chars", {}).get(self.ln, "Employee name contains invalid characters"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_department(self):
        fun_message = self.cloud_message.get("check_department", {})

        department_id = self.request_data.get("department_id")

        if department_id is None:
            self.error_handling.append({
                "tap": 1,
                "field": "department_id",
                "error": fun_message.get("required", {}).get(self.ln, "Department is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        try:
            from backend_apps.departments.models import Department
            Department.objects.get(id=department_id)
        except:
            self.error_handling.append({
                "tap": 1,
                "field": "department_id",
                "error": fun_message.get("not_found", {}).get(self.ln, "Department not found"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_company(self):
        fun_message = self.cloud_message.get("check_company", {})

        company_id = self.request_data.get("company_id")

        if company_id is None:
            self.error_handling.append({
                "tap": 1,
                "field": "company_id",
                "error": fun_message.get("required", {}).get(self.ln, "Company is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        try:
            from backend_apps.companies.models import Company
            Company.objects.get(id=company_id)
        except:
            self.error_handling.append({
                "tap": 1,
                "field": "company_id",
                "error": fun_message.get("not_found", {}).get(self.ln, "Company not found"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_user(self):
        fun_message = self.cloud_message.get("check_user", {})

        user_id = self.request_data.get("user_id")

        if user_id is None:
            return True

        try:
            from backend_apps.users.models import UserAccounts
            UserAccounts.objects.get(id=user_id)
        except:
            self.error_handling.append({
                "tap": 1,
                "field": "user_id",
                "error": fun_message.get("not_found", {}).get(self.ln, "User not found"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_mobile(self):
        fun_message = self.cloud_message.get("check_mobile", {})

        mobile = self.request_data.get("mobile")

        if mobile is None:
            return True

        try:
            int(mobile)
        except:
            self.error_handling.append({
                "tap": 1,
                "field": "mobile",
                "error": fun_message.get("invalid", {}).get(self.ln, "Invalid mobile number"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_email(self, exclude_user_id=None):
        fun_message = self.cloud_message.get("check_user_create", {})

        email = self.request_data.get("email", "").strip()

        if not email:
            self.error_handling.append({
                "tap": 1,
                "field": "email",
                "error": fun_message.get("email_required", {}).get(self.ln, "Email is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            self.error_handling.append({
                "tap": 1,
                "field": "email",
                "error": fun_message.get("email_invalid", {}).get(self.ln, "Invalid email format"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        from backend_apps.users.models import UserAccounts

        email_exists = UserAccounts.objects.filter(email=email)
        if exclude_user_id:
            email_exists = email_exists.exclude(id=exclude_user_id)
        if email_exists.exists():
            self.error_handling.append({
                "tap": 1,
                "field": "email",
                "error": fun_message.get("email_exists", {}).get(self.ln, "Email already exists"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_password(self):
        fun_message = self.cloud_message.get("check_user_create", {})

        password = self.request_data.get("password", "").strip()

        if not password:
            self.error_handling.append({
                "tap": 1,
                "field": "password",
                "error": fun_message.get("password_required", {}).get(self.ln, "Password is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def delete(self, pk=None):
        fun_message = self.cloud_message.get("check_delete", {})

        try:
            model_object = self.modelDB.get(id=pk)
        except:
            return status.HTTP_404_NOT_FOUND, fun_message.get("not_found", {}).get(self.ln, "Employee not found"), None

        related_objects = []
        for rel in model_object._meta.related_objects:
            related_name = rel.get_accessor_name()
            related_manager = getattr(model_object, related_name)
            if related_manager.exists():
                related_objects.append(rel.related_model._meta.verbose_name_plural.title())

        if related_objects:
            self.error_handling.append({
                "tap": 1,
                "field": "delete",
                "error": fun_message.get("related_objects_found", {}).get(self.ln, "Cannot delete: related objects exist"),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, {', '.join(related_objects)}

        try:
            with transaction.atomic():
                model_object.delete()
        except Exception as e:
            self.error_handling.append({
                "tap": 1,
                "field": "delete",
                "error": str(e),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"errors": self.error_handling}, None

        return status.HTTP_200_OK, fun_message.get("deleted_successfully", {}).get(self.ln, "Employee deleted successfully"), None

    def create(self):
        object_info = None

        if not self.check_name():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_company():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_department():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_email():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_password():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_mobile():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        try:
            with transaction.atomic():
                from backend_apps.users.models import UserAccounts

                name = self.request_data.get("name", "").strip()
                email = self.request_data.get("email", "").strip()
                password = self.request_data.get("password", "").strip()

                username = name.replace(" ", "").lower() + str(UserAccounts.objects.count() + 1)

                user = UserAccounts.objects.create(
                    username=username,
                    email=email,
                    first_name=name.split()[0] if name else "",
                    last_name=" ".join(name.split()[1:]) if len(name.split()) > 1 else "",
                    role=RoleChoices.EMPLOYEE,
                    company_id=self.request_data.get("company_id"),
                )
                user.set_password(password)
                user.save()

                model_object = Employee.objects.create(
                    name=name,
                    department_id=self.request_data.get("department_id"),
                    user=user,
                    title=self.request_data.get("title"),
                    mobile=self.request_data.get("mobile"),
                    address=self.request_data.get("address"),
                )

                status_code, message, data = self.view(model_object=model_object)
                if status_code == status.HTTP_200_OK:
                    object_info = data["object_info"]
        except Exception as e:
            self.error_handling.append({
                "tap": 1,
                "field": "create",
                "error": str(e),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"errors": self.error_handling}, None

        success_message = self.cloud_message.get("create_success", {}).get(self.ln, "Employee created successfully")
        return status.HTTP_200_OK, success_message, {
            "object_info": object_info,
            "error_handling": self.error_handling,
        }

    def update(self, pk=None):
        object_info = None

        try:
            model_object = self.modelDB.get(id=pk)
        except:
            return status.HTTP_404_NOT_FOUND, self.cloud_message.get("not_found", {}).get(self.ln, "Not found!"), None

        name = self.request_data.get("name")
        department_id = self.request_data.get("department_id")
        user_id = self.request_data.get("user_id")

        if name:
            if not self.check_name():
                return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if department_id is not None:
            if not self.check_department():
                return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        email = self.request_data.get("email")
        if email is not None:
            if not self.check_email(exclude_user_id=model_object.user.id if model_object.user else None):
                return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_mobile():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        try:
            with transaction.atomic():
                if name:
                    model_object.name = name.strip()
                if department_id is not None:
                    model_object.department_id = department_id
                if user_id is not None:
                    model_object.user_id = user_id
                if self.request_data.get("title") is not None:
                    model_object.title = self.request_data.get("title")
                if self.request_data.get("mobile") is not None:
                    model_object.mobile = self.request_data.get("mobile")
                if self.request_data.get("address") is not None:
                    model_object.address = self.request_data.get("address")

                if email is not None and model_object.user:
                    model_object.user.email = email.strip()
                    model_object.user.save()

                model_object.save()

                status_code, message, data = self.view(model_object=model_object)
                if status_code == status.HTTP_200_OK:
                    object_info = data["object_info"]
        except Exception as e:
            self.error_handling.append({
                "tap": 1,
                "field": "update",
                "error": str(e),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"errors": self.error_handling}, None

        success_message = self.cloud_message.get("update_success", {}).get(self.ln, "Employee updated successfully")
        return status.HTTP_200_OK, success_message, {
            "object_info": object_info,
            "error_handling": self.error_handling,
        }

    def update_status(self, pk=None):
        object_info = None

        try:
            model_object = self.modelDB.get(id=pk)
        except:
            return status.HTTP_404_NOT_FOUND, self.cloud_message.get("not_found", {}).get(self.ln, "Not found!"), None

        is_active = self.request_data.get("is_active")
        if is_active is None:
            self.error_handling.append({
                "tap": 1,
                "field": "is_active",
                "error": self.cloud_message.get("check_status", {}).get(self.ln, "Status is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        try:
            with transaction.atomic():
                model_object.user.is_active = is_active
                model_object.user.save()

                status_code, message, data = self.view(model_object=model_object)
                if status_code == status.HTTP_200_OK:
                    object_info = data["object_info"]
        except Exception as e:
            self.error_handling.append({
                "tap": 1,
                "field": "update_status",
                "error": str(e),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"errors": self.error_handling}, None

        success_message = self.cloud_message.get("update_status_success", {}).get(self.ln, "Employee status updated successfully")
        return status.HTTP_200_OK, success_message, {
            "object_info": object_info,
            "error_handling": self.error_handling,
        }
