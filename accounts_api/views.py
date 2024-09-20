from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import InvestmentAccount, Transaction
from .serializers import InvestmentAccountSerializer, TransactionSerializer
from .permissions import IsViewOnly, IsFullAccess, IsPostOnly

from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.utils.dateparse import parse_date


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [IsViewOnly]
        elif self.action in ["create", "update", "destroy"]:
            self.permission_classes = [IsFullAccess]
        return super().get_permissions()


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_permissions(self):
        account_id = self.request.data.get("account")
        try:
            account = InvestmentAccount.objects.get(id=account_id)
        except InvestmentAccount.DoesNotExist:
            raise serializers.ValidationError("Invalid account ID.")

        if account.account_type == "view_only":
            self.permission_classes = [IsViewOnly]
        elif account.account_type == "post_only":
            self.permission_classes = [IsPostOnly]
        elif account.account_type == "full_access":
            self.permission_classes = [IsFullAccess]

        return super().get_permissions()


class AdminViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def transactions_summary(self, request):
        user = request.user
        accounts = InvestmentAccount.objects.filter(users=user)

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        transactions = Transaction.objects.filter(account__in=accounts)
        if start_date:
            transactions = transactions.filter(timestamp__gte=parse_date(start_date))
        if end_date:
            transactions = transactions.filter(timestamp__lte=parse_date(end_date))

        total_balance = transactions.aggregate(Sum("amount"))["amount__sum"] or 0

        return Response(
            {
                "total_balance": total_balance,
                "transactions": TransactionSerializer(transactions, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


def dashboard(request):
    return render(request, "index.html")
