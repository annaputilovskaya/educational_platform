from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.datetime_safe import datetime

from config.settings import EMAIL_HOST_USER


@shared_task
def send_mail_about_course_updating(email_list, course):
    """
    Отправляет письмо об обновления курса пользователю.
    """

    # Преобразование даты в удобный вид.
    updated_at = datetime.strftime(timezone.now(), "%d.%m.%Y %H:%M")

    # Создание текста письма и отправка его на адреса подписчиков.
    message = f"Курc {course} обновлен {updated_at}."
    send_mail("Обновление курса", message, EMAIL_HOST_USER, email_list)
