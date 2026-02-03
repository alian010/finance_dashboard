from django.contrib import admin
from .models import Transaction, TransactionCategory


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "code")
    prepopulated_fields = {"code": ("name",)}


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "category", "amount", "deleted_at", "created_at")
    list_filter = ("category", "date", "deleted_at")
    search_fields = ("user__username", "user__email", "note")
    date_hierarchy = "date"
    ordering = ("-date", "-id")
    readonly_fields = ("created_at", "updated_at", "deleted_at")

    actions = ["restore_transactions", "hard_delete_transactions"]

    def get_queryset(self, request):
        # ✅ show all including deleted
        return Transaction.all_objects.all()

    @admin.action(description="Restore selected transactions")
    def restore_transactions(self, request, queryset):
        queryset.update(deleted_at=None)

    @admin.action(description="Hard delete selected transactions (PERMANENT)")
    def hard_delete_transactions(self, request, queryset):
        # ✅ real delete safely
        Transaction.all_objects.filter(pk__in=queryset.values_list("pk", flat=True)).delete()
