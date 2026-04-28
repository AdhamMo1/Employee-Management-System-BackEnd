from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backend_apps.users.core.users import UserHandle
from backend_apps.users.shared_utils.decorators import admin_required, hr_or_admin_required, authenticated_required


class UsersAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_status = status.HTTP_400_BAD_REQUEST
        self.response_message = ""
        self.response_data = None

    @authenticated_required()
    def get(self, request, pk=None):
        if pk:
            call_response = UserHandle(request).view(pk)
        else:
            item_id = request.GET.get('id')
            if item_id:
                call_response = UserHandle(request).view(item_id)
            else:
                call_response = UserHandle(request).all()

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])

    @hr_or_admin_required()
    def post(self, request):
        call_response = UserHandle(request).create()

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])

    @admin_required()
    def put(self, request, pk=None):
        call_response = UserHandle(request).update(pk)

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])

    @hr_or_admin_required()
    def patch(self, request, pk=None):
        call_response = UserHandle(request).update_status(pk)

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])

    @admin_required()
    def delete(self, request, pk=None):
        call_response = UserHandle(request).delete(pk)

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])
