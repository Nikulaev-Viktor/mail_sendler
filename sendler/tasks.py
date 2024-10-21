import smtplib
from django.core.mail import send_mail
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from sendler.models import MailSettings, Log


def send_mailing():
    """Функция отправки рассылки"""
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = MailSettings.objects.filter(first_time_send__lte=current_datetime, status__in=['LAUNCHED'],
                                           is_active=True)
    for mailing in mailings:

        if mailing.first_time_send <= current_datetime:
            status = 'NOT_SUCCESSFUL'
            server_response = 'Письмо не было отправлено'

            try:
                clients = [client.email for client in mailing.clients.all()]
                send_mail(
                    subject=mailing.message.message_title,
                    message=mailing.message.message_text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=clients,
                    fail_silently=False
                )

                if mailing.periodicity == 'DAILY':
                    mailing.first_time_send += timedelta(days=1)
                elif mailing.periodicity == 'WEEKLY':
                    mailing.first_time_send += timedelta(days=7)
                elif mailing.periodicity == 'MONTHLY':
                    mailing.first_time_send += timedelta(days=30)

                mailing.save()

                status = 'SUCCESSFUL'
                server_response = 'Письмо успешно отправлено'

            except smtplib.SMTPException as e:
                status = False
                server_response = str(e)

            finally:
                Log.objects.create(
                    date_last_attempt=datetime.now(zone),
                    attempt_status=status,
                    server_response=server_response,
                    mailing=mailing,
                )
