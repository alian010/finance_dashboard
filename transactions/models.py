from django.conf import settings
from django.db import models
from django.utils import timezone


class TransactionType(models.TextChoices):
    INCOME = "INCOME", "Income"
    EXPENSE = "EXPENSE", "Expense"


class TransactionCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.SlugField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(deleted_at=timezone.now())

    def alive(self):
        return self.filter(deleted_at__isnull=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    # ✅ default দিলাম যাতে makemigrations এ prompt না আসে
    txn_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        default=TransactionType.EXPENSE,
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    note = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["-date", "-id"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "txn_type", "date"]),
            models.Index(fields=["user", "date", "category"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gt=0), name="transaction_amount_gt_0"),
        ]

    def delete(self, using=None, keep_parents=False):
        if self.deleted_at is None:
            self.deleted_at = timezone.now()
            self.save(update_fields=["deleted_at"])
