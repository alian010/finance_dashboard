from django.db.models import Sum
from django.utils import timezone

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Transaction, TransactionCategory, TransactionType
from .serializers import TransactionSerializer, TransactionCategorySerializer
from .permissions import IsOwner
from .pagination import TransactionPagination


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = TransactionPagination

    def get_queryset(self):
        # ✅ default manager already hides deleted
        return Transaction.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        # ✅ soft delete (calls model.delete override)
        instance.delete()


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = TransactionCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TransactionCategory.objects.filter(is_active=True).order_by("name")


class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        start = today.replace(day=1)

        qs = Transaction.objects.filter(
            user=request.user,
            date__gte=start,
            date__lte=today
        )

        income_total = qs.filter(txn_type=TransactionType.INCOME).aggregate(s=Sum("amount"))["s"] or 0
        expense_total = qs.filter(txn_type=TransactionType.EXPENSE).aggregate(s=Sum("amount"))["s"] or 0
        net = income_total - expense_total

        income_breakdown_qs = (
            qs.filter(txn_type=TransactionType.INCOME)
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )
        expense_breakdown_qs = (
            qs.filter(txn_type=TransactionType.EXPENSE)
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        income_breakdown = {row["category__name"]: float(row["total"]) for row in income_breakdown_qs}
        expense_breakdown = {row["category__name"]: float(row["total"]) for row in expense_breakdown_qs}

        return Response({
            "month_start": str(start),
            "month_end": str(today),
            "income_total": float(income_total),
            "expense_total": float(expense_total),
            "net": float(net),
            "income_breakdown": income_breakdown,
            "expense_breakdown": expense_breakdown,
        })
