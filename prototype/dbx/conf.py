from appconf import AppConf

from django.conf import settings


class ProfileConf(AppConf):
    URL_PREFIX = 'dbx'
    settings.DBX['FILES_ENDPOINT'] = 'https://api.dropboxapi.com/2/files/list_folder'
