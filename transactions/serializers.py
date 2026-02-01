from django.utils import timezone
from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "amount", "date", "category", "note", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_amount(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_date(self, value):
        today = timezone.localdate()
        if value > today:
            raise serializers.ValidationError("Date cannot be in the future.")
        return value

    def create(self, validated_data):
        # owner-only: server sets user, not client
        request = self.context["request"]
        return Transaction.objects.create(user=request.user, **validated_data)
