# Generated by Django 4.2 on 2024-07-12 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0003_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата последнего обновления"
            ),
        ),
    ]
