# Generated by Django 5.0.6 on 2024-07-10 06:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_amount', models.IntegerField(default=0)),
                ('delivery_date', models.DateField()),
                ('order_status', models.CharField(choices=[('Running', 'Running'), ('Submitted', 'Submitted'), ('Completed', 'Completed')], max_length=100)),
                ('post_title', models.CharField(max_length=500)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_orders', to=settings.AUTH_USER_MODEL)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='freelancer_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]