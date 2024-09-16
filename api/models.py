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
