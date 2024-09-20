from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import InvestmentAccount, Transaction


class AccountPermissionsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="password123")

        self.post_only_account = InvestmentAccount.objects.create(
            name="Post Only Account", account_type="post_only"
        )
        self.post_only_account.users.add(self.user)

        self.client = APIClient()
        self.client.login(username="user1", password="password123")

        self.transactions_url = reverse("transaction-list")

    def test_post_only_account_can_post_transaction(self):
        """Ensure post-only account can POST a transaction."""
        data = {"account": self.post_only_account.id, "amount": 100.0}
        response = self.client.post(self.transactions_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_only_account_cannot_get_transactions(self):
        """Ensure post-only account cannot GET transactions."""
        response = self.client.get(
            self.transactions_url, {"account": self.post_only_account.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Post-only accounts cannot view transactions.", response.data["detail"]
        )

    def test_post_only_account_cannot_update_transaction(self):
        """Ensure post-only account cannot UPDATE a transaction."""
        transaction = Transaction.objects.create(
            account=self.post_only_account, amount=100.0
        )
        update_url = reverse("transaction-detail", args=[transaction.id])
        response = self.client.put(update_url, {"amount": 200.0}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Post-only accounts can only perform POST requests.",
            response.data["detail"],
        )

    def test_post_only_account_cannot_delete_transaction(self):
        """Ensure post-only account cannot DELETE a transaction."""
        transaction = Transaction.objects.create(
            account=self.post_only_account, amount=100.0
        )
        delete_url = reverse("transaction-detail", args=[transaction.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Post-only accounts can only perform POST requests.",
            response.data["detail"],
        )
