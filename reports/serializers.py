from rest_framework import serializers


class SummaryResponseSerializer(serializers.Serializer):
    current_month_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    category_breakdown = serializers.DictField(child=serializers.DecimalField(max_digits=12, decimal_places=2))
    trend_percent = serializers.FloatField()
