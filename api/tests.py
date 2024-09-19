from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, InvestmentAccount, UserInvestmentAccount, Transaction
from django.contrib.auth import get_user_model

User = get_user_model()


class InvestmentAccountPermissionTests(APITestCase):
    def setUp(self):
        # Create users
        self.user_viewer = User.objects.create_user(
            username="view", password="password"
        )
        self.user_poster = User.objects.create_user(
            username="post", password="password"
        )
        self.user_manager = User.objects.create_user(
            username="full crud", password="password"
        )

        self.investment_account = InvestmentAccount.objects.create(
            name="Test Account", balance=1000.00
        )

        UserInvestmentAccount.objects.create(
            user=self.user_viewer,
            investment_account=self.investment_account,
            role="VIEW",
        )
        UserInvestmentAccount.objects.create(
            user=self.user_poster,
            investment_account=self.investment_account,
            role="POST",
        )
        UserInvestmentAccount.objects.create(
            user=self.user_manager,
            investment_account=self.investment_account,
            role="FULL CRUD",
        )

        self.transaction = Transaction.objects.create(
            investment_account=self.investment_account, amount=100.00, date="2024-01-01"
        )

    def test_viewer_can_view_investment_account(self):
        self.client.login(username="view", password="password")
        url = reverse(
            "investment_account_detail", kwargs={"pk": self.investment_account.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_viewer_cannot_post_transactions(self):
        self.client.login(username="view", password="password")
        url = reverse("transaction_create")
        data = {
            "investment_account": self.investment_account.pk,
            "amount": 50.00,
            "date": "2024-01-02",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewer_cannot_update_investment_account(self):
        self.client.login(username="view", password="password")
        url = reverse(
            "investment_account_detail", kwargs={"pk": self.investment_account.pk}
        )
        data = {"name": "Updated Account", "balance": 2000.00}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_poster_can_post_transactions(self):
        self.client.login(username="post", password="password")
        url = reverse("transaction_create")
        data = {
            "investment_account": self.investment_account.pk,
            "amount": 150.00,
            "date": "2024-01-03",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_poster_cannot_view_investment_account(self):
        self.client.login(username="post", password="password")
        url = reverse(
            "investment_account_detail", kwargs={"pk": self.investment_account.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_poster_cannot_update_investment_account(self):
        self.client.login(username="post", password="password")
        url = reverse(
            "investment_account_detail", kwargs={"pk": self.investment_account.pk}
        )
        data = {"name": "Updated Account", "balance": 3000.00}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_view_investment_account(self):
        self.client.login(username="full crud", password="password")
        url = reverse(
            "investment_account_detail", kwargs={"pk": self.investment_account.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_can_update_investment_account(self):
        self.client.login(username="full crud", password="password")
        url = reverse(
            "investment_account_detail", kwargs={"pk": self.investment_account.pk}
        )
        data = {"name": "Updated Account", "balance": 4000.00}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_can_delete_investment_account(self):
        self.client.login(username="full crud", password="password")
        url = reverse(
            "investment_account_detail", kwargs={"pk": self.investment_account.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_manager_can_post_transactions(self):
        self.client.login(username="full crud", password="password")
        url = reverse("transaction_create")
        data = {
            "investment_account": self.investment_account.pk,
            "amount": 200.00,
            "date": "2024-01-04",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_authorized_user_cannot_access(self):
        url = reverse(
            "investment_account_detail", kwargs={"pk": self.investment_account.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
