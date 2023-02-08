# Generated by Django 4.1.6 on 2023-02-04 16:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("book_service", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowings",
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
                ("borrow_date", models.DateTimeField()),
                (
                    "expected_return_date",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2023, 2, 5, 16, 46, 14, 556182, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
                ("actual_return_date", models.DateTimeField()),
                (
                    "book_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="borrowings",
                        to="book_service.book",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="borrowings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Borrowings",
                "verbose_name_plural": "Borrowings",
                "ordering": ["expected_return_date"],
            },
        ),
    ]