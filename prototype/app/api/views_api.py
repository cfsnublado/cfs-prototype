import dropbox
from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

from core.api.views_api import APIDefaultsMixin


def get_dropbox_object():
    dbx_token = settings.DBX['ACCESS_TOKEN']
    dbx = dropbox.Dropbox(dbx_token)

    return dbx


def upload_dbx(local_filepath, dbx_filepath):
    pass


class UploadView(APIDefaultsMixin, APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = request.data

        if 'file' not in data:
            raise ParseError('Empty content')

        f = data['file']

        upload_dir = settings.TMP_DIR
        filename = f.name
        dest_file_path = upload_dir / filename
        dbx = get_dropbox_object()

        with open(dest_file_path, 'wb') as tmp_upload_file:
            for chunk in f.chunks():
                tmp_upload_file.write(chunk)

        with open(dest_file_path, 'rb') as dbx_upload_file:
            try:
                dbx_dest_path = '/{0}/{1}'.format(request.user.id, filename)
                dbx.files_upload(
                    dbx_upload_file.read(),
                    dbx_dest_path,
                    mode=WriteMode('overwrite')
                )
            except ApiError as err:
                # This checks for the specific error where a user doesn't have enough
                # Dropbox space quota to upload this file.
                if (err.error.is_path() and err.error.get_path().error.is_insufficient_space()):
                    print("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                else:
                    print(err)

        return Response(data={}, status=status.HTTP_200_OK)
