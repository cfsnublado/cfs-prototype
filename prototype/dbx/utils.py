import dropbox
from dropbox.files import WriteMode

from django.conf import settings


def get_dbx_object():
    dbx_token = settings.DBX['ACCESS_TOKEN']
    dbx = dropbox.Dropbox(dbx_token)

    return dbx


def upload_file_to_dbx(local_filepath, dbx_filepath, create_shared_link=False):
    dbx = get_dbx_object()

    with open(local_filepath, 'rb') as upload_file:
        dbx.files_upload(
            upload_file.read(),
            dbx_filepath,
            mode=WriteMode('overwrite')
        )

    if create_shared_link:
        shared_link = dbx.sharing_create_shared_link(
            path=dbx_filepath,
            short_url=False,
            pending_upload=None
        )
        print(shared_link)
