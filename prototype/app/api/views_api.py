from dropbox.exceptions import ApiError
from rest_framework import status
from rest_framework.exceptions import APIException, ParseError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

from core.api.views_api import APIDefaultsMixin
from dbx.utils import upload_file_to_dbx


class UploadView(APIDefaultsMixin, APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = request.data

        if 'file' not in data:
            raise ParseError('Empty content')

        file = data['file']

        upload_dir = settings.TMP_DIR
        tmp_filepath = upload_dir / file.name
        dbx_filepath = '/{0}/{1}'.format(request.user.id, file.name)

        with open(tmp_filepath, 'wb') as tmp_upload_file:
            for chunk in file.chunks():
                tmp_upload_file.write(chunk)

        try:
            upload_file_to_dbx(tmp_filepath, dbx_filepath)
        except ApiError:
            raise APIException('Upload dbx error')

        return Response(data={}, status=status.HTTP_200_OK)
