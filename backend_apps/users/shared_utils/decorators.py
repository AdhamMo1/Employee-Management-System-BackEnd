from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from backend_apps.users.shared_utils import message_manager


def get_message(key, default, ln="en"):
    return message_manager.message.get("decorators", {}).get(key, {}).get(ln, default)


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            ln = request.META.get("HTTP_LN", "en")
            if ln not in message_manager.languages:
                ln = "en"

            if not request.user or not request.user.is_authenticated:
                return Response(
                    {
                        'details': get_message("auth_required", "Authentication required.", ln),
                        'data': None
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if request.user.role not in roles:
                required = " or ".join(roles)
                return Response(
                    {
                        'details': get_message("permission_denied", "Permission denied.", ln) + f" Required role: {required}",
                        'data': None
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def authenticated_required():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            ln = request.META.get("HTTP_LN", "en")
            if ln not in message_manager.languages:
                ln = "en"

            if not request.user or not request.user.is_authenticated:
                return Response(
                    {
                        'details': get_message("auth_required", "Authentication required.", ln),
                        'data': None
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required():
    return role_required('SYSTEM_ADMINISTRATOR')


def hr_or_admin_required():
    return role_required('SYSTEM_ADMINISTRATOR', 'HR_MANAGER')
