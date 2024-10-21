from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from sendler.apps import SendlerConfig
from sendler.views import IndexView, ContactsView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailSettingsListView, MailSettingsDetailView, MailSettingsCreateView, MailSettingsUpdateView, \
    MailSettingsDeleteView, LogListView

app_name = SendlerConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),

    path('client/', cache_page(60)(ClientListView.as_view()), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('message/', cache_page(60)(MessageListView.as_view()), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mail_settings/', cache_page(60)(MailSettingsListView.as_view()), name='mail_settings_list'),
    path('mail_settings/<int:pk>/', MailSettingsDetailView.as_view(), name='mail_settings_detail'),
    path('mail_settings/create/', MailSettingsCreateView.as_view(), name='mail_settings_create'),
    path('mail_settings/<int:pk>/update/', MailSettingsUpdateView.as_view(), name='mail_settings_update'),
    path('mail_settings/<int:pk>/delete/', MailSettingsDeleteView.as_view(), name='mail_settings_delete'),

    path('log_list/', LogListView.as_view(), name='log_list'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
