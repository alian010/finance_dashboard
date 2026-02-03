from django.utils import timezone
from rest_framework import serializers
from .models import Transaction, TransactionCategory, TransactionType


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ("id", "name", "code", "is_active")


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_code = serializers.CharField(source="category.code", read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "txn_type",
            "amount",
            "date",
            "category",
            "category_name",
            "category_code",
            "note",
            "created_at",
            "updated_at",
            "deleted_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "category_name", "category_code")

    def validate_amount(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_date(self, value):
        today = timezone.localdate()
        if value > today:
            raise serializers.ValidationError("Date cannot be in the future.")
        return value

    def validate_txn_type(self, value):
        if value not in (TransactionType.INCOME, TransactionType.EXPENSE):
            raise serializers.ValidationError("Invalid txn_type.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        return Transaction.all_objects.create(user=request.user, **validated_data)
