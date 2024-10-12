from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email='admin@example.com', first_name='admin', country='Россия')
        user.set_password('123qwe456')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
