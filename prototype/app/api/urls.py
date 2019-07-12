from django.urls import path
from django.conf.urls import include

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from dbx.api.views_api import UploadAudioDbxView
from users.api.views_api import UserViewSet, ProfileViewSet

app_name = 'app'

router = DefaultRouter()

# users
router.register('user', UserViewSet, base_name='user')
router.register('profile', ProfileViewSet, base_name='profile')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='auth_token'),
    path('upload-audio-dbx/', UploadAudioDbxView.as_view(), name='upload_audio_dbx'),
    path('', include(router.urls)),
]
