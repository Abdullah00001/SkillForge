# Generated by Django 5.0.6 on 2024-07-11 17:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('skills', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=150)),
                ('post_description', models.TextField()),
                ('budget', models.IntegerField(default=0)),
                ('deadline', models.DateField()),
                ('post_creation_time', models.DateTimeField(auto_now_add=True)),
                ('post_status', models.CharField(choices=[('Open', 'Open'), ('Close', 'Close')], max_length=80)),
                ('post_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('required_skill', models.ManyToManyField(to='skills.skills')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
