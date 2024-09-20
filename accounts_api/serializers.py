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

        if not account.users.filter(id=user.id).exists():
            raise serializers.ValidationError(
                "Invalid account ID or insufficient access rights."
            )

        if account.account_type == "view_only":
            if request.method != "GET":
                raise serializers.ValidationError(
                    "View-only accounts cannot perform this action."
                )

        elif account.account_type == "post_only":
            if request.method == "POST":
                return data
            else:
                raise serializers.ValidationError(
                    "Post-only accounts cannot perform this action."
                )

        elif account.account_type == "full_access":
            return data

        raise serializers.ValidationError("Invalid account type for this action.")


class InvestmentAccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = InvestmentAccount
        fields = ["id", "name", "account_type", "transactions"]
