from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from sendler.apps import SendlerConfig
from sendler.views import IndexView

app_name = SendlerConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
