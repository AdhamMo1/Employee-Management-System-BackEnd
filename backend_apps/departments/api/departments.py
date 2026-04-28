from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backend_apps.departments.core.departments import DepartmentHandle
from backend_apps.users.shared_utils.decorators import hr_or_admin_required


class DepartmentsAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_status = status.HTTP_400_BAD_REQUEST
        self.response_message = ""
        self.response_data = None

    @hr_or_admin_required()
    def get(self, request, pk=None):
        if pk:
            call_response = DepartmentHandle(request).view(pk)
        else:
            item_id = request.GET.get('id')
            if item_id:
                call_response = DepartmentHandle(request).view(item_id)
            else:
                call_response = DepartmentHandle(request).all()

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])

    @hr_or_admin_required()
    def post(self, request):
        call_response = DepartmentHandle(request).create()

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])

    @hr_or_admin_required()
    def put(self, request, pk=None):
        call_response = DepartmentHandle(request).update(pk)

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])

    @hr_or_admin_required()
    def delete(self, request, pk=None):
        call_response = DepartmentHandle(request).delete(pk)

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])
