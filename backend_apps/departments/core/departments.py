import json
import re

from rest_framework import status
from django.db import transaction

from backend_apps.departments.models import Department
from backend_apps.departments.shared_utils import message_manager


class DepartmentHandle:
    def __init__(self, request):
        self.request = request
        self.error_handling = []
        self.cloud_message = message_manager.message.get("departments", {})

        requested_language = self.request.META.get("HTTP_LN", "en")
        self.ln = requested_language if requested_language in message_manager.languages else "en"

        self.modelDB = Department.objects.all()
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
                "company_id": model_object.company.id if model_object.company else None,
                "company_name": model_object.company.name if model_object.company else None,
                "name": model_object.name,
                "created_at": model_object.created_at,
                "updated_at": model_object.updated_at,
            }
        else:
            return status.HTTP_404_NOT_FOUND, self.cloud_message.get("not_found", {}).get(self.ln, "Not found!"), None

        success_message = self.cloud_message.get("view_success", {}).get(self.ln, "Department retrieved successfully")
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
            response_data["list_items"].append(self.view(model_object=model_object)[2]["object_info"])

        success_message = self.cloud_message.get("all_success", {}).get(self.ln, "Departments retrieved successfully")
        return status.HTTP_200_OK, success_message, response_data

    def check_name(self, object_id=None):
        fun_message = self.cloud_message.get("check_name", {})

        name = self.request_data.get("name", "").strip()

        if not name:
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("required", {}).get(self.ln, "Department name is required"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if len(name) < 2:
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("min_length", {}).get(self.ln, "Department name must be at least 2 characters long"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if len(name) > 255:
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("max_length", {}).get(self.ln, "Department name must not exceed 255 characters"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        if not re.match(r'^[\w\s\-\.&]+$', name):
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("invalid_chars", {}).get(self.ln, "Department name contains invalid characters"),
                "index_main": 0,
                "index_sub": 0
            })
            return False

        queryset = self.modelDB.filter(name__iexact=name)
        if object_id:
            queryset = queryset.exclude(id=object_id)
        if queryset.exists():
            self.error_handling.append({
                "tap": 1,
                "field": "name",
                "error": fun_message.get("duplicate", {}).get(self.ln, "A department with this name already exists"),
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

    def delete(self, pk=None):
        fun_message = self.cloud_message.get("check_delete", {})

        try:
            model_object = self.modelDB.get(id=pk)
        except:
            return status.HTTP_404_NOT_FOUND, fun_message.get("not_found", {}).get(self.ln, "Department not found"), None

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

        return status.HTTP_200_OK, fun_message.get("deleted_successfully", {}).get(self.ln, "Department deleted successfully"), None

    def create(self):
        object_info = None

        if not self.check_name():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if not self.check_company():
            return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        try:
            with transaction.atomic():
                model_object = Department.objects.create(
                    name=self.request_data.get("name").strip(),
                    company_id=self.request_data.get("company_id")
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

        success_message = self.cloud_message.get("create_success", {}).get(self.ln, "Department created successfully")
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
        company_id = self.request_data.get("company_id")

        if name:
            if not self.check_name(object_id=model_object.id):
                return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        if company_id is not None:
            if not self.check_company():
                return status.HTTP_400_BAD_REQUEST, {"errors": self.error_handling}, None

        try:
            with transaction.atomic():
                if name:
                    model_object.name = name.strip()
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

        success_message = self.cloud_message.get("update_success", {}).get(self.ln, "Department updated successfully")
        return status.HTTP_200_OK, success_message, {
            "object_info": object_info,
            "error_handling": self.error_handling,
        }
