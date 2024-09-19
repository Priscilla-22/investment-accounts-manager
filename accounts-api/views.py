from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import InvestmentAccount, Transaction
from .serializers import InvestmentAccountSerializer, TransactionSerializer
from .permissions import IsViewOnly, IsFullAccess, IsPostOnly

from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if (
            self.action == "retrieve"
            and self.request.user.accounts.filter(account_type="view_only").exists()
        ):
            self.permission_classes = [IsViewOnly]
        elif (
            self.action in ["create", "update", "delete"]
            and self.request.user.accounts.filter(account_type="full_access").exists()
        ):
            self.permission_classes = [IsFullAccess]
        elif (
            self.action == "create"
            and self.request.user.accounts.filter(account_type="post_only").exists()
        ):
            self.permission_classes = [IsPostOnly]
        return super().get_permissions()


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


class AdminViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def transactions_summary(self, request):
        user = request.user
        accounts = InvestmentAccount.objects.filter(user=user)
        transactions = Transaction.objects.filter(account__in=accounts)
        total_balance = transactions.aggregate(Sum("amount"))["amount__sum"] or 0

        return Response(
            {
                "total_balance": total_balance,
                "transactions": TransactionSerializer(transactions, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


from django.shortcuts import render


def dashboard(request):
    return render(request, "index.html")
