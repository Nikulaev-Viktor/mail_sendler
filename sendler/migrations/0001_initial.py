# Generated by Django 4.2 on 2024-10-15 16:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        help_text="Введите имя клиента",
                        max_length=150,
                        null=True,
                        verbose_name="Имя",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        help_text="Введите фамилию клиента",
                        max_length=150,
                        null=True,
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Введите email клиента",
                        max_length=254,
                        verbose_name="email получателя",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        help_text="Комментарий",
                        null=True,
                        verbose_name="комментарий",
                    ),
                ),
            ],
            options={
                "verbose_name": "Получатель",
                "verbose_name_plural": "Получатели",
                "ordering": ["first_name", "email"],
            },
        ),
        migrations.CreateModel(
            name="Log",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_last_attempt",
                    models.DateTimeField(
                        auto_now=True, verbose_name=" дата и время последней попытки"
                    ),
                ),
                (
                    "attempt_status",
                    models.CharField(
                        choices=[
                            ("SUCCESSFUL", "успешно"),
                            ("NOT_SUCCESSFUL", "не успешно"),
                        ],
                        max_length=50,
                        verbose_name="статус попытки",
                    ),
                ),
                (
                    "server_response",
                    models.TextField(
                        blank=True, null=True, verbose_name="ответ сервера"
                    ),
                ),
            ],
            options={
                "verbose_name": "лог",
                "verbose_name_plural": "логи",
            },
        ),
        migrations.CreateModel(
            name="MailSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_time_send",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="дата и время первой отправки рассылки",
                    ),
                ),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("DAILY", "ежедневно"),
                            ("WEEKLY", "еженедельно"),
                            ("MONTHLY", "ежемесячно"),
                        ],
                        default="DAILY",
                        help_text="Выберете периодичность рассылки",
                        max_length=50,
                        verbose_name="Периодичность рассылки",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("CREATE", "создана"),
                            ("LAUNCHED", "запущена"),
                            ("COMPLETED", "завершена"),
                        ],
                        default="CREATE",
                        help_text="статус рассылки",
                        max_length=50,
                        verbose_name="статус рассылки",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Активация рассылки"
                    ),
                ),
            ],
            options={
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
                "permissions": [
                    ("can_view_mailsettings", "может просматривать настройки рассылки"),
                    ("can_edit_mailsettings", "может отключать/включать рассылки"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "message_title",
                    models.CharField(
                        help_text="Тема сообщения",
                        max_length=250,
                        verbose_name="тема сообщения",
                    ),
                ),
                (
                    "message_text",
                    models.TextField(
                        help_text="Сообщение", verbose_name="текст сообщения"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата создания"
                    ),
                ),
                (
                    "update_at",
                    models.DateTimeField(auto_now=True, verbose_name="дата обновления"),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ["message_title"],
            },
        ),
    ]
