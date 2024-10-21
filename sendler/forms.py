from django.forms import ModelForm, BooleanField, DateTimeInput

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
        fields = ('email', 'first_name', 'last_name', 'comment', 'owner')


class MessageForm(StyleFormMixin, ModelForm):
    """Форма редактирования сообщения"""

    class Meta:
        model = Message
        fields = ('message_title', 'message_text', 'owner')


class MailSettingsForm(StyleFormMixin, ModelForm):
    """Форма редактирования настройки рассылки"""

    class Meta:
        model = MailSettings
        fields = '__all__'
        widgets = {
            'first_time_send': DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'type': 'datetime-local'})
        }


class LogView(StyleFormMixin, ModelForm):
    """Форма редактирования попытки рассылки"""

    class Meta:
        model = Log
        fields = ('attempt_status',)


class MailSettingsModeratorForm(StyleFormMixin, ModelForm):
    """Форма редактирования настройки рассылки для модераторов"""

    class Meta:
        model = MailSettings
        fields = ('is_active',)
