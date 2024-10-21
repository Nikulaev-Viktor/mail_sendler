from django.utils import timezone

from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Клиент сервиса"""
    first_name = models.CharField(max_length=150, verbose_name='Имя', help_text='Введите имя клиента', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', help_text='Введите фамилию клиента',
                                 **NULLABLE)
    email = models.EmailField(verbose_name='email получателя', help_text='Введите email клиента')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE, help_text='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.last_name} {self.first_name}: {self.email}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['first_name', 'email']


class Message(models.Model):
    """Сообщение для рассылки"""
    message_title = models.CharField(max_length=250, verbose_name='тема сообщения', help_text='Тема сообщения')
    message_text = models.TextField(verbose_name='текст сообщения', help_text='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.message_title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['message_title']


class MailSettings(models.Model):
    """Настройки Рассылки"""
    CHOICES_PERIODICITY = (
        ('DAILY', 'ежедневно'),
        ('WEEKLY', 'еженедельно'),
        ('MONTHLY', 'ежемесячно'),
    )
    CHOICES_STATUS = (
        ('CREATE', 'создана'),
        ('LAUNCHED', 'запущена'),
        ('COMPLETED', 'завершена'),
    )
    first_time_send = models.DateTimeField(default=timezone.now, verbose_name='дата и время первой отправки рассылки')
    periodicity = models.CharField(max_length=50, default='DAILY', verbose_name='Периодичность рассылки',
                                   choices=CHOICES_PERIODICITY, help_text='Выберете периодичность рассылки')
    status = models.CharField(max_length=50, default='CREATE', verbose_name='статус рассылки', choices=CHOICES_STATUS,
                              help_text='статус рассылки')
    is_active = models.BooleanField(default=True, verbose_name='Активация рассылки')
    clients = models.ManyToManyField(Client, verbose_name='клиенты', help_text='выберете клиентов для рассылки',
                                     related_name='mailings')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение',
                                help_text='выберете сообщение', related_name='mailings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

        permissions = permissions = [
            ('can_view_mail_settings', 'Может просматривать рассылки'),
            ('can_change_mail_settings', 'Может отключать рассылки'),
            ('can_view_user', 'Может просматривать пользователей'),
            ('can_block_user', 'Может блокировать пользователей')
        ]


class Log(models.Model):
    """Логи рассылки"""
    STATUS_SEND = (
        ('SUCCESSFUL', 'успешно'),
        ('NOT_SUCCESSFUL', 'не успешно'),
    )
    date_last_attempt = models.DateTimeField(auto_now=True, verbose_name=' дата и время последней попытки')
    attempt_status = models.CharField(max_length=50, choices=STATUS_SEND, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ сервера', **NULLABLE)
    mailing = models.ForeignKey(MailSettings, on_delete=models.CASCADE, verbose_name='рассылка', related_name='logs')

    def __str__(self):
        return f'{self.date_last_attempt} {self.attempt_status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
