# Generated by Django 5.0.6 on 2024-07-11 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('post', '0001_initial'),
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category'),
        ),
        migrations.AlterField(
            model_name='post',
            name='required_skill',
            field=models.ManyToManyField(to='skills.skills'),
        ),
    ]