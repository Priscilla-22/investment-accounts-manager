from rest_framework import serializers
from .models import InvestmentAccount, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "amount", "timestamp", "account"]

    def validate(self, data):
        account = data.get("account")
        request = self.context["request"]
        user = request.user

        # Check if the user has access to the account
        if not account.users.filter(id=user.id).exists():
            raise serializers.ValidationError(
                "Invalid account ID or insufficient access rights."
            )

        # Check permissions based on account type
        if account.account_type == "view_only" and request.method == "POST":
            raise serializers.ValidationError(
                "View-only accounts cannot create transactions."
            )
        elif account.account_type == "post_only" and request.method != "POST":
            raise serializers.ValidationError(
                "Post-only accounts cannot view or modify transactions."
            )

        return data


class InvestmentAccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = InvestmentAccount
        fields = ["id", "name", "account_type", "transactions"]
