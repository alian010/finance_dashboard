from django.conf import settings
from django.db import models


class TransactionCategory(models.TextChoices):
    FOOD = "FOOD", "Food"
    RENT = "RENT", "Rent"
    TRANSPORT = "TRANSPORT", "Transport"
    ENTERTAINMENT = "ENTERTAINMENT", "Entertainment"
    UTILITIES = "UTILITIES", "Utilities"
    HEALTH = "HEALTH", "Health"
    SHOPPING = "SHOPPING", "Shopping"
    EDUCATION = "EDUCATION", "Education"
    OTHER = "OTHER", "Other"


class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=32, choices=TransactionCategory.choices)
    note = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-id"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "category", "date"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gt=0),
                name="transaction_amount_gt_0",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user_id} | {self.date} | {self.category} | {self.amount}"
