from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from .models import InvestmentAccount, Transaction, User, UserInvestmentAccount
from .permissions import (
    ViewInvestmentAccountPermission,
    PostTransactionPermission,
)
from .serializers import InvestmentAccountSerializer, TransactionSerializer


def get_user_role(user, investment_account):
    try:
        user_investment_account = UserInvestmentAccount.objects.get(
            user=user, investment_account=investment_account
        )
        return user_investment_account.role
    except UserInvestmentAccount.DoesNotExist:
        return None


class InvestmentAccountListView(APIView):
    permission_classes = [ViewInvestmentAccountPermission]

    def get(self, request):
        investment_accounts = InvestmentAccount.objects.all()
        serializer = InvestmentAccountSerializer(investment_accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InvestmentAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvestmentAccountDetailView(APIView):
    def get(self, request, pk):
        investment_account = get_object_or_404(InvestmentAccount, pk=pk)
        role = get_user_role(request.user, investment_account)

        if role == "VIEW" or role == "FULL CRUD":
            serializer = InvestmentAccountSerializer(investment_account)
            return Response(serializer.data)
        return Response(
            {"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )

    def put(self, request, pk):
        investment_account = get_object_or_404(InvestmentAccount, pk=pk)
        role = get_user_role(request.user, investment_account)

        if role == "FULL CRUD":
            serializer = InvestmentAccountSerializer(
                investment_account, data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )

    def delete(self, request, pk):
        investment_account = get_object_or_404(InvestmentAccount, pk=pk)
        role = get_user_role(request.user, investment_account)

        if role == "FULL CRUD":
            investment_account.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )


class TransactionCreateView(APIView):
    permission_classes = [PostTransactionPermission]

    def post(self, request):
        investment_account_id = request.data.get("investment_account")
        investment_account = get_object_or_404(
            InvestmentAccount, id=investment_account_id
        )
        role = get_user_role(request.user, investment_account)

        if role == "POST" or role == "FULL CRUD":
            serializer = TransactionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )


class AdminTransactionView(APIView):
    def get(self, request):
        user = request.user
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        transactions = Transaction.objects.filter(investment_account__users=user)
        if start_date and end_date:
            transactions = transactions.filter(date__range=[start_date, end_date])

        total_balance = transactions.aggregate(Sum("amount"))["amount__sum"]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(
            {"transactions": serializer.data, "total_balance": total_balance}
        )


class UserTransactionView(APIView):
    def get(self, request, pk):
        investment_account = get_object_or_404(InvestmentAccount, pk=pk)
        transactions = Transaction.objects.filter(investment_account=investment_account)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class InvestmentAccountUserView(APIView):
    def get(self, request, pk):
        investment_account = get_object_or_404(InvestmentAccount, pk=pk)
        users = investment_account.users.all()
        user_ids = [user.id for user in users]
        return Response(user_ids)

    def post(self, request, pk):
        investment_account = get_object_or_404(InvestmentAccount, pk=pk)
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        investment_account.users.add(user)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        investment_account = get_object_or_404(InvestmentAccount, pk=pk)
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        investment_account.users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
