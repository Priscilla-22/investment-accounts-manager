from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    investment_accounts = models.ManyToManyField("InvestmentAccounts")


class InvestmentAccount(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    users = models.ManyToManyField(User)


class Transaction(models.Model):
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()


class UserInvestmentAccount(models.Model):
    PERMISSIONS = [
        ("VIEW", "View"),
        ("FULL CRUD", "full crud"),
        ("POST", "Post"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=PERMISSIONS)

    class Meta:
        unique_together = ("user", "investment_account")
