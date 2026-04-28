from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backend_apps.companies.core.dashboard import DashboardHandle
from backend_apps.users.shared_utils.decorators import hr_or_admin_required


class DashboardAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_status = status.HTTP_400_BAD_REQUEST
        self.response_message = ""
        self.response_data = None

    @hr_or_admin_required()
    def get(self, request):
        call_response = DashboardHandle(request).get_stats()

        re_send = {
            'details': call_response[1],
            'data': call_response[2],
        }
        return Response(re_send, call_response[0])
