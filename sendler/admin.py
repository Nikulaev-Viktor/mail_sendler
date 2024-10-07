from django.contrib import admin

from sendler.models import Client, Message, MailSettings, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_filter = ('email',)
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_title', 'created_at', 'update_at')
    search_fields = ('message_title',)


@admin.register(MailSettings)
class MailSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_time_send', 'periodicity', 'status', 'message')
    list_filter = ('periodicity', 'status', 'clients', 'message')
    search_fields = ('status', 'client', 'message')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_last_attempt', 'attempt_status', 'server_response', 'mailing')
    list_filter = ('attempt_status', 'server_response', 'mailing')
    search_fields = ('server_response',)




