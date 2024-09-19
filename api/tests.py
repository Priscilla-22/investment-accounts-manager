from django.test import TestCase
from django.contrib.auth.models import User
from .models import InvestmentAccount, Transaction


class InvestmentAccountTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.account = InvestmentAccount.objects.create(
            user=self.user, name="Test Account", account_type="full_access"
        )

    def test_create_transaction(self):
        transaction = Transaction.objects.create(account=self.account, amount=100)
        self.assertEqual(transaction.amount, 100)
