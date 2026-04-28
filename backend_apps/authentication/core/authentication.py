from ..shared_utils.authentication_manager import UserAuthenticationManager
from backend_apps.authentication.shared_utils import message_manager
from backend_apps.users.models import UserAccounts
from django.contrib.auth import authenticate
from rest_framework import status


class AuthenticationHandle:
    def __init__(self, request):
        self.request = request

        # Default response values
        self.response_status = status.HTTP_400_BAD_REQUEST
        self.response_message = ""
        self.response_data = None

        # Load language based messages from the message manager
        self.message = message_manager.message["authentication"]

        requested_language = self.request.META.get("HTTP_LN", "en")
        self.ln = requested_language if requested_language in message_manager.languages else "en"

    def check_email(self, email=None):
        if email is None:
            email = self.request.POST.get("email", "").strip().lower()

        try:
            user_object = UserAccounts.objects.get(email=email)
        except UserAccounts.DoesNotExist:
            user_object = None

        if user_object:
            if user_object.is_active:
                self.response_status = status.HTTP_200_OK
            else:
                self.response_status = status.HTTP_400_BAD_REQUEST
                self.response_message = self.message["check_email"]["not_active"][self.ln]
                user_object = None
        else:
            self.response_status = status.HTTP_404_NOT_FOUND
            self.response_message = self.message["check_email"]["not_found"][self.ln]

        # never put user_object in response_data
        return self.response_status, self.response_message, user_object

    def login(self):
        check_email = self.check_email()
        self.response_status, self.response_message, user_object = check_email[0], check_email[1], check_email[2]
        # Proceed only if the user exists
        if self.response_status == status.HTTP_200_OK:
            self.response_status = status.HTTP_400_BAD_REQUEST

            # Authenticate the user using the provided password
            auth_user = authenticate(
                username=user_object.username,
                email=user_object.email,
                password=self.request.POST.get("password"),
                backend='django.contrib.auth.backends.ModelBackend'
            )
            # If authentication is successful
            if auth_user:
                open_user_manager = UserAuthenticationManager(self.request)

                open_user_manager.handle_response(user_object)

                # Set the returned values from the manager to the current instance
                self.response_status = open_user_manager.response_status
                self.response_message = open_user_manager.response_message
                self.response_data = open_user_manager.response_data
            else:
                self.response_status = status.HTTP_400_BAD_REQUEST
                self.response_message = self.message["check_password"]["incorrect_password"][self.ln]

        # Return the final status, message, and data
        return self.response_status, self.response_message, self.response_data
