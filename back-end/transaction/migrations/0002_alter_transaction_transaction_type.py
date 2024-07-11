# Generated by Django 5.0.6 on 2024-07-11 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('Deposit', 'Deposit'), ('Withdraw', 'Withdraw'), ('Payment', 'Payment'), ('Receive', 'Receive')], max_length=50),
        ),
    ]
