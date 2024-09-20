from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import InvestmentAccount, Transaction


class AdminViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.account = InvestmentAccount.objects.create(name="Test Account")
        self.account.users.add(self.user)

        Transaction.objects.create(account=self.account, amount=100.00)
        Transaction.objects.create(account=self.account, amount=150.00)

        self.client.login(username="testuser", password="testpass")

    def test_transactions_summary(self):
        url = reverse("admin-transactions-summary")  # Adjust to your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_balance"], 250.00)
