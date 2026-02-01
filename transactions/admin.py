from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "category", "amount", "created_at")
    list_filter = ("category", "date")
    search_fields = ("user__username", "user__email", "note")
    date_hierarchy = "date"
    ordering = ("-date", "-id")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("user", "amount", "date", "category")}),
        ("Optional", {"fields": ("note",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
