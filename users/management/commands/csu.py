from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда создания администратора (суперпользователя).
    """

    def handle(self, *args, **kwargs):
        user = User.objects.create(email="admin@sky.pro")
        user.set_password("admin-1")
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
