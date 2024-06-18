# Generated by Django 4.2 on 2024-06-18 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
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
                    "title",
                    models.CharField(max_length=255, verbose_name="Название курса"),
                ),
                (
                    "preview",
                    models.ImageField(blank=True, null=True, upload_to="lms/course"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Описание курса"
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
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
                    "title",
                    models.CharField(max_length=255, verbose_name="Название урока"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Описание урока"
                    ),
                ),
                (
                    "preview",
                    models.ImageField(blank=True, null=True, upload_to="lms/lesson"),
                ),
                (
                    "video_link",
                    models.URLField(
                        blank=True, null=True, verbose_name="Ссылка на видео"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lms.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
    ]
