# Generated by Django 5.1.1 on 2024-09-19 06:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinvestmentaccount',
            name='user',
        ),
        migrations.RemoveField(
            model_name='investmentaccount',
            name='users',
        ),
        migrations.AlterUniqueTogether(
            name='userinvestmentaccount',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='userinvestmentaccount',
            name='investment_account',
        ),
        migrations.RemoveField(
            model_name='investmentaccount',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='date',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='investment_account',
        ),
        migrations.AddField(
            model_name='investmentaccount',
            name='account_type',
            field=models.CharField(choices=[('view_only', 'View Only'), ('full_access', 'Full Access'), ('post_only', 'Post Only')], default='view_only', max_length=20),
        ),
        migrations.AddField(
            model_name='investmentaccount',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.investmentaccount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='UserInvestmentAccount',
        ),
    ]
