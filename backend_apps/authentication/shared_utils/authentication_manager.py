from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from backend_apps.authentication.shared_utils import message_manager


class UserAuthenticationManager:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.ln = request.headers.get("ln", "en")
        self.response_status = status.HTTP_200_OK
        self.response_message = ""
        self.response_data = None
        self.message = message_manager.message["authentication"]
        requested_language = self.request.META.get("HTTP_LN", "en")
        self.ln = requested_language if requested_language in message_manager.languages else "en"

    def _message(self, section, key):
        return self.message[section][key][self.ln]

    def handle_status(self):
        self.response_status = status.HTTP_401_UNAUTHORIZED

        if not self.user.is_active:
            self.response_message = self._message("check_email", "not_active")
            return

        if self.user.role not in [
            self.user.Role.SYSTEM_ADMIN,
            self.user.Role.HR_MANAGER,
            self.user.Role.EMPLOYEE,
        ]:
            self.response_message = self._message("check_email", "not_found")
            return

        self.response_status = status.HTTP_200_OK

    def handle_response(self, user_object):
        self.response_status = status.HTTP_401_UNAUTHORIZED

        if not user_object:
            self.response_status = status.HTTP_404_NOT_FOUND
            self.response_message = self._message("check_email", "not_found")
            return

        refresh = RefreshToken.for_user(user_object)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        try:
            company_id = user_object.company.id
            employee_id = user_object.employee.id
        except:
            company_id = None
            employee_id = None

        self.response_status = status.HTTP_200_OK
        self.response_data = {
            "session": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            "user_info": {
                "id": user_object.id,
                "email": user_object.email,
                "role": user_object.role,
                "employee_id": employee_id,
                "company_id": company_id,
            },
        }

    def response(self):
        return self.response_status, self.response_message, self.response_data