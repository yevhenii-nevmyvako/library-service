from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from book_service.models import Book
from user.models import User


class Borrowings(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=False, default=date.today)
    expected_return_date = models.DateTimeField(
        auto_now_add=False,
    )
    actual_return_date = models.DateTimeField(
        auto_now_add=False, blank=True, null=True
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="borrowings"
    )

    @staticmethod
    def validate_date(
        borrow_date: date,
        expected_return_date: date,
        actual_return_date: date,
        error_to_raise,
    ):
        if borrow_date > expected_return_date:
            raise error_to_raise(
                f"{borrow_date}Borrow date should not be later than {expected_return_date}"
            )

        if actual_return_date and borrow_date > actual_return_date:
            raise error_to_raise(
                f"{borrow_date} should not be later than {actual_return_date}"
            )

    def clean(self):
        self.validate_date(
            self.borrow_date,
            self.expected_return_date,
            self.actual_return_date,
            ValidationError,
        )

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)

    def book_info(self):
        return self.book

    def user_full_name(self):
        return self.user

    class Meta:
        ordering = ["expected_return_date"]
        verbose_name_plural = "Borrowings"
        verbose_name = "Borrowings"

    def __str__(self):
        return f"{self.user} borrowed {self.book} {self.borrow_date}"
