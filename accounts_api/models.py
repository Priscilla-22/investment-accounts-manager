from django.contrib.auth.models import User
from django.db import models


class InvestmentAccount(models.Model):
    ACCOUNT_TYPES = (
        ("view_only", "View Only"),
        ("full_access", "Full Access"),
        ("post_only", "Post Only"),
    )

    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="accounts")
    account_type = models.CharField(
        max_length=20, choices=ACCOUNT_TYPES, default="view_only"
    )

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"


class Transaction(models.Model):
    account = models.ForeignKey(
        InvestmentAccount,
        related_name="transactions",
        on_delete=models.CASCADE,
        null=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.account.name}: {self.amount}"
