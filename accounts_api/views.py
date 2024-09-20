from rest_framework import viewsets, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils.dateparse import parse_date
from django.shortcuts import render

from .models import InvestmentAccount, Transaction
from .serializers import InvestmentAccountSerializer, TransactionSerializer
from .permissions import IsViewOnly, IsFullAccess, IsPostOnly


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Set permissions based on the account type.
        """
        account_id = self.kwargs.get("pk")  
        if account_id:
            account = InvestmentAccount.objects.filter(id=account_id).first()
            if (
                account
                and account.account_type == "post_only"
                and self.request.method == "GET"
            ):
                self.permission_classes = [IsPostOnly] 
        return super().get_permissions()


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Override to set specific permissions for actions.
        """
        if self.action in ["retrieve", "list"]:  
            account_id = self.request.query_params.get("account")
            if account_id:
                account = InvestmentAccount.objects.filter(id=account_id).first()
                if account and account.account_type == "post_only":
                    self.permission_classes = [IsPostOnly]
        return super().get_permissions()

    def check_post_only_permission(self, account, request):
        """
        Helper method to check if the account is 'post_only' and block non-POST requests.
        """
        if account.account_type == "post_only" and request.method != "POST":
            raise serializers.ValidationError(
                "Post-only accounts can only perform POST requests."
            )

    def perform_create(self, serializer):
        """
        Custom method to check 'post_only' restrictions before creating a transaction.
        """
        account = serializer.validated_data.get("account")
        self.check_post_only_permission(account, self.request)
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Block update operation for 'post_only' accounts.
        """
        transaction = self.get_object()
        account = transaction.account
        self.check_post_only_permission(account, request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Block delete operation for 'post_only' accounts.
        """
        transaction = self.get_object()
        account = transaction.account
        self.check_post_only_permission(account, request)
        return super().destroy(request, *args, **kwargs)


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
