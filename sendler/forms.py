from django.forms import BooleanField
from django import forms
from django.forms import ModelForm, BooleanField

from sendler.models import Client, Message, MailSettings, Log


class StyleFormMixin:
    """Миксин для стилизации формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, ModelForm):
    """Форма редактирования клиента"""

    class Meta:
        model = Client
        fields = ('email', 'first_name', 'last_name', 'comment')


class MessageForm(StyleFormMixin, ModelForm):
    """Форма редактирования сообщения"""

    class Meta:
        model = Message
        fields = ('message_title', 'message_text', 'owner')


class MailSettingsForm(StyleFormMixin, ModelForm):
    """Форма редактирования настройки рассылки"""

    class Meta:
        model = MailSettings
        fields = ('periodicity', 'first_time_send', 'status', 'message', 'clients')


class LogView(StyleFormMixin, ModelForm):
    """Форма редактирования попытки рассылки"""

    class Meta:
        model = Log
        fields = ('attempt_status',)


class MailSettingsModeratorForm(StyleFormMixin, ModelForm):

    class Meta:
        model = MailSettings
        exclude = ('owner',)
