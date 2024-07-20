from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """
    Модель курса.
    """

    title = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(upload_to="lms/course", **NULLABLE)
    description = models.TextField(verbose_name="Описание курса", **NULLABLE)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE
    )
    updated_at = models.DateTimeField(
        auto_now=True, **NULLABLE, verbose_name="Дата последнего обновления"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.title}"


class Lesson(models.Model):
    """
    Модель урока.
    """

    title = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", **NULLABLE)
    preview = models.ImageField(upload_to="lms/lesson", **NULLABLE)
    video_link = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.title}"


class Subscription(models.Model):
    """
    Модель подписки на информирование об обновлении курса.
    """

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self):
        return f"Подписка {self.user} на курс {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
