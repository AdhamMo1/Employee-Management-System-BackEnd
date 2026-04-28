from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend_apps.authentication.core.authentication import AuthenticationHandle


@api_view(["POST", ])
@permission_classes([AllowAny])
def login_api(request):
    call_response = AuthenticationHandle(request).login()
    re_send = {
        'details': call_response[1],
        'data': call_response[2],
    }
    return Response(re_send, call_response[0])