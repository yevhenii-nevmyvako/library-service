from django.db import models

from borrowings_service.models import Borrowings


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    class TypeChoices(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    type = models.CharField(max_length=10, choices=TypeChoices.choices)
    borrowing = models.ForeignKey(
        Borrowings, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField(max_length=255)
    session_id = models.CharField(max_length=255, unique=True)
    money_to_pay = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        ordering = ("-money_to_pay",)
        verbose_name = "Payments"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Session id: {self.session_id} " \
               f"Money to pay {self.money_to_pay}"
