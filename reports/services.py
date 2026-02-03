from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from transactions.models import Transaction, TransactionType


def month_range(date):
    start = date.replace(day=1)
    # next month start
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1, day=1)
    else:
        end = start.replace(month=start.month + 1, day=1)
    return start, end


def breakdown_by_category(qs):
    rows = (
        qs.values("category__name")
        .annotate(total=Coalesce(Sum("amount"), 0))
        .order_by("-total")
    )
    return {r["category__name"]: float(r["total"]) for r in rows}


def get_monthly_summary(user, for_date=None):
    today = for_date or timezone.localdate()
    start, end = month_range(today)

    base = Transaction.objects.filter(user=user, date__gte=start, date__lt=end)

    income_qs = base.filter(txn_type=TransactionType.INCOME)
    expense_qs = base.filter(txn_type=TransactionType.EXPENSE)

    total_income = income_qs.aggregate(s=Coalesce(Sum("amount"), 0))["s"]
    total_expense = expense_qs.aggregate(s=Coalesce(Sum("amount"), 0))["s"]

    return {
        "month": start.strftime("%Y-%m"),
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "net": float(total_income - total_expense),
        "income_breakdown": breakdown_by_category(income_qs),
        "expense_breakdown": breakdown_by_category(expense_qs),
    }
