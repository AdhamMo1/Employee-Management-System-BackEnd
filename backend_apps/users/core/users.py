import json
import re

from rest_framework import status
from django.db import transaction

from backend_apps.users.models import UserAccounts, RoleChoices
from backend_apps.users.shared_utils import message_manager


class UserHandle:
    def __init__(self, request):
        self.request = request
        self.error_handling = []
        self.cloud_message = message_manager.message.get("users", {})

        requested_language = self.request.META.get("HTTP_LN", "en")
        self.ln = requested_language if requested_language in message_manager.languages else "en"

        self.modelDB = UserAccounts.objects.all()
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
            full_name = model_object.first_name
            if model_object.last_name:
                full_name = f"{model_object.first_name} {model_object.last_name}"

            object_info = {
                "id": model_object.id,
                "username": model_object.username,
                "email": model_object.email,
                "name": full_name,
                "first_name": model_object.first_name,
                "last_name": model_object.last_name,
                "role": model_object.role,
                "is_active": model_object.is_active,
                "company_id": model_object.company.id if model_object.company else None,
                "company_name": model_object.company.name if model_object.company else None,
                "created_at": model_object.created_at,
                "updated_at": model_object.updated_at,
            }
        else:
            return status.HTTP_404_NOT_FOUND, self.cloud_message.get("not_found", {}).get(self.ln, "Not found!"), None

        success_message = self.cloud_message.get("view_success", {}).get(self.ln, "User retrieved successfully")
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

        queryset = self.modelDB.order_by('-updated_at', '-created_at')

        if self.request.GET.get("company_id"):
            queryset = queryset.filter(company_id=self.request.GET.get("company_id"))

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
            full_name = model_object.first_name
            if model_object.last_name:
                full_name = f"{model_object.first_name} {model_object.last_name}"

            response_data["list_items"].append(self.view(model_object=model_object)[2]["object_info"])

        success_message = self.cloud_message.get("all_success", {}).get(self.ln, "Users retrieved successfully")
        return status.HTTP_200_OK, success_message, response_data

    def check_username(self, exclude_user_id=None):
        fun_message = self.cloud_message.get("check_username", {})

        username = self.request_data.get("username", "").strip()

        if not username:
            self.error_handling.append({
                "tap": 1,
                "field": "username",
                "error": fun_message.get("required", {}).get(self.ln, "Username is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if len(username) < 3:
            self.error_handling.append({
                "tap": 1,
                "field": "username",
                "error": fun_message.get("min_length", {}).get(self.ln, "Username must be at least 3 characters long"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if len(username) > 150:
            self.error_handling.append({
                "tap": 1,
                "field": "username",
                "error": fun_message.get("max_length", {}).get(self.ln, "Username must not exceed 150 characters"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if not re.match(r'^[\w.@+-]+$', username):
            self.error_handling.append({
                "tap": 1,
                "field": "username",
                "error": fun_message.get("invalid_chars", {}).get(self.ln, "Username contains invalid characters"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        username_exists = self.modelDB.filter(username=username)
        if exclude_user_id:
            username_exists = username_exists.exclude(id=exclude_user_id)
        if username_exists.exists():
            self.error_handling.append({
                "tap": 1,
                "field": "username",
                "error": fun_message.get("exists", {}).get(self.ln, "Username already exists"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_email(self, exclude_user_id=None):
        fun_message = self.cloud_message.get("check_email", {})

        email = self.request_data.get("email", "").strip()

        if not email:
            self.error_handling.append({
                "tap": 1,
                "field": "email",
                "error": fun_message.get("required", {}).get(self.ln, "Email is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            self.error_handling.append({
                "tap": 1,
                "field": "email",
                "error": fun_message.get("invalid", {}).get(self.ln, "Invalid email format"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        email_exists = self.modelDB.filter(email=email)
        if exclude_user_id:
            email_exists = email_exists.exclude(id=exclude_user_id)
        if email_exists.exists():
            self.error_handling.append({
                "tap": 1,
                "field": "email",
                "error": fun_message.get("exists", {}).get(self.ln, "Email already exists"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_password(self):
        fun_message = self.cloud_message.get("check_password", {})

        password = self.request_data.get("password", "").strip()

        if not password:
            self.error_handling.append({
                "tap": 1,
                "field": "password",
                "error": fun_message.get("required", {}).get(self.ln, "Password is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if len(password) < 8:
            self.error_handling.append({
                "tap": 1,
                "field": "password",
                "error": fun_message.get("min_length", {}).get(self.ln, "Password must be at least 8 characters long"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_name(self):
        fun_message = self.cloud_message.get("check_name", {})

        name = self.request_data.get("name", "").strip()

        if not name:
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("required", {}).get(self.ln, "Name is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        return True

    def check_company(self):
        fun_message = self.cloud_message.get("check_company", {})

        company_id = self.request_data.get("company_id")

        if company_id is None:
            return True

        if self.request_data.get("role") == RoleChoices.SYSTEM_ADMINISTRATOR:
            return True

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

    def check_role(self):
        fun_message = self.cloud_message.get("check_role", {})

        role = self.request_data.get("role")

        if role is None:
            self.error_handling.append({
                "tap": 1,
                "field": "role",
                "error": fun_message.get("required", {}).get(self.ln, "Role is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        allowed_roles = [
            RoleChoices.SYSTEM_ADMINISTRATOR,
            RoleChoices.HR_MANAGER,
        ]
        if role not in allowed_roles:
            self.error_handling.append({
                "tap": 1,
                "field": "role",
                "error": fun_message.get("invalid", {}).get(self.ln, "Role must be System Administrator or HR Manager"),
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
            return status.HTTP_404_NOT_FOUND, fun_message.get("not_found", {}).get(self.ln, "User not found"), None

        if self.request.user and self.request.user.id == model_object.id:
            self.error_handling.append({
                "tap": 1,
                "field": "delete",
                "error": fun_message.get("cannot_delete_self", {}).get(self.ln, "Cannot delete your own account"),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_403_FORBIDDEN, {"errors": self.error_handling}, None

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

        return status.HTTP_200_OK, fun_message.get("deleted_successfully", {}).get(self.ln, "User deleted successfully"), None

    def create(self):
        object_info = None

        if not self.check_name():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_email():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_password():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_company():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_role():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        try:
            with transaction.atomic():
                email = self.request_data.get("email", "").strip()
                username = email.split('@')[0].lower() + str(UserAccounts.objects.count() + 1)

                name = self.request_data.get("name", "").strip()
                name_parts = name.split()
                first_name = name_parts[0] if name_parts else ""
                last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

                model_object = UserAccounts.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role=self.request_data.get("role", RoleChoices.NOT_SELECTED),
                    company_id=self.request_data.get("company_id", None) if self.request_data.get("company_id", None) else None,
                )
                model_object.set_password(self.request_data.get("password").strip())
                model_object.save()

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

        success_message = self.cloud_message.get("create_success", {}).get(self.ln, "User created successfully")
        return status.HTTP_201_CREATED, success_message, {
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
        email = self.request_data.get("email")
        company_id = self.request_data.get("company_id")
        role = self.request_data.get("role")

        if name is not None:
            if not self.check_name():
                return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if email is not None:
            if not self.check_email(exclude_user_id=model_object.id):
                return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if company_id is not None:
            if not self.check_company():
                return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if role is not None:
            if not self.check_role():
                return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        try:
            with transaction.atomic():
                if name is not None:
                    name_parts = name.strip().split()
                    model_object.first_name = name_parts[0] if name_parts else ""
                    model_object.last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                if email is not None:
                    model_object.email = email.strip()
                if role is not None:
                    model_object.role = role
                if company_id is not None:
                    model_object.company_id = company_id

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

        success_message = self.cloud_message.get("update_success", {}).get(self.ln, "User updated successfully")
        return status.HTTP_200_OK, success_message, {
            "object_info": object_info,
            "error_handling": self.error_handling,
        }

    def update_status(self, pk):
        fun_message = self.cloud_message.get("check_update_status", {})

        try:
            model_object = self.modelDB.get(id=pk)
        except:
            self.error_handling.append({
                "tap": 1,
                "field": "id",
                "error": self.cloud_message.get("not_found", {}).get(self.ln, "Not found!"),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_404_NOT_FOUND, {"errors": self.error_handling}, None

        if self.request.user and self.request.user.id == model_object.id:
            self.error_handling.append({
                "tap": 1,
                "field": "is_active",
                "error": fun_message.get("cannot_update_self_status", {}).get(self.ln, "Cannot update your own status"),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_403_FORBIDDEN, {"errors": self.error_handling}, None

        status_value = self.request_data.get("is_active")

        try:
            with transaction.atomic():
                if isinstance(status_value, bool):
                    model_object.is_active = status_value
                elif str(status_value).strip().lower() in ["true", "1"]:
                    model_object.is_active = True
                else:
                    model_object.is_active = False

                model_object.save()

                status_code, message, data = self.view(model_object=model_object)
                if status_code == status.HTTP_200_OK:
                    success_message = self.cloud_message.get("update_status_success", {}).get(self.ln, "User status updated successfully")
                    return status.HTTP_200_OK, success_message, {"object_info": data["object_info"]}
        except Exception as e:
            self.error_handling.append({
                "tap": 1,
                "field": "update_status",
                "error": str(e),
                "index_main": 0,
                "index_sub": 0
            })
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"errors": self.error_handling}, None

        return status_code, message, data
