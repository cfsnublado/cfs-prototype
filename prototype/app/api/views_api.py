from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.views_api import APIDefaultsMixin


class UploadView(APIDefaultsMixin, APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)

        return Response(data={}, status=status.HTTP_200_OK)
