from django.contrib import admin

# Register your models here.
from .models import InvestmentAccount, Transaction


@admin.register(InvestmentAccount)
class InvestmentAccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "account_type",
    )
    search_fields = (
        "name",
        "account_type",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "amount",
        "timestamp",
    )
    list_filter = ("timestamp",)
    search_fields = ("account__name",)
