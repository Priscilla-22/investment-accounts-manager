from rest_framework import serializers
from .models import InvestmentAccount, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "amount", "timestamp"]


class InvestmentAccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = InvestmentAccount
        fields = ["id", "name", "account_type", "transactions"]
