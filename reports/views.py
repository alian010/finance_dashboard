from datetime import date
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from transactions.models import Transaction
from .serializers import SummaryResponseSerializer


class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        user = request.user

        # current month range
        current_start = today.replace(day=1)
        if current_start.month == 12:
            current_end = date(current_start.year + 1, 1, 1)
        else:
            current_end = date(current_start.year, current_start.month + 1, 1)

        # previous month range
        if current_start.month == 1:
            prev_start = date(current_start.year - 1, 12, 1)
        else:
            prev_start = date(current_start.year, current_start.month - 1, 1)
        prev_end = current_start

        current_qs = Transaction.objects.filter(user=user, date__gte=current_start, date__lt=current_end)
        prev_qs = Transaction.objects.filter(user=user, date__gte=prev_start, date__lt=prev_end)

        current_total = current_qs.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        prev_total = prev_qs.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        # category breakdown
        breakdown_rows = (
            current_qs.values("category")
            .annotate(total=Sum("amount"))
            .order_by()
        )
        breakdown = {row["category"]: (row["total"] or Decimal("0.00")) for row in breakdown_rows}

        # trend percent
        if prev_total == 0:
            trend_percent = 0.0 if current_total == 0 else 100.0
        else:
            trend_percent = float(((current_total - prev_total) / prev_total) * 100)

        payload = {
            "current_month_total": current_total,
            "category_breakdown": breakdown,
            "trend_percent": trend_percent,
        }

        # optional schema validation
        SummaryResponseSerializer(data=payload).is_valid(raise_exception=True)
        return Response(payload)
