from rest_framework import serializers
from .models import InvestmentAccount, Transaction


class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = ["id", "name", "balance", "users"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "investment_account", "amount", "date"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["investment_account"] = instance.investment_account.name
        return representation
