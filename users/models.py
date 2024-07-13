from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Модель пользователя.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE)
    city = models.CharField(max_length=50, verbose_name="Город", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Аватар", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """
    Модель платежа.
    """

    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Наличными"),
        ("TRANSFER", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", **NULLABLE
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Урок", **NULLABLE
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма")
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default="TRANSFER",
        verbose_name="Способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
