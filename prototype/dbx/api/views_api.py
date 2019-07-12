import magic
from dropbox.exceptions import ApiError
from rest_framework import status
from rest_framework.exceptions import APIException, ParseError, UnsupportedMediaType
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

from core.api.views_api import APIDefaultsMixin
from ..utils import upload_file_to_dbx


def check_in_memory_mime(in_memory_file):
    mime = magic.from_buffer(
        in_memory_file.read(),
        mime=True
    )

    return mime


class UploadDbxView(
    APIDefaultsMixin, APIView
):
    permission_classes = [IsAdminUser]
    allowed_mime_types = [
        'text/plain', 'text/markdown',
        'application/pdf', 'audio/mpeg'
    ]
    create_shared_link = False

    def post(self, request, *args, **kwargs):
        data = request.data

        if 'file' not in data:
            raise ParseError('Empty content')

        file = data['file']
        mime = check_in_memory_mime(file)

        if mime not in self.allowed_mime_types:
            raise UnsupportedMediaType(mime)

        upload_dir = settings.TMP_DIR
        tmp_filepath = upload_dir / file.name
        # Upload to user subfolder in app identified by user id (UUID)
        dbx_filepath = '/{0}/{1}'.format(request.user.id, file.name)

        with open(tmp_filepath, 'wb') as tmp_upload_file:
            for chunk in file.chunks():
                tmp_upload_file.write(chunk)

        try:
            upload_file_to_dbx(
                tmp_filepath,
                dbx_filepath,
                create_shared_link=self.create_shared_link
            )
        except ApiError:
            raise APIException('Upload dbx error')

        return Response(data={}, status=status.HTTP_200_OK)


class UploadAudioDbxView(UploadDbxView):
    allowed_mime_types = ['audio/mpeg']
    create_shared_link = True
