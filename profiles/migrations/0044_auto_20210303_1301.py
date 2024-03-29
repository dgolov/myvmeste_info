# Generated by Django 3.1.5 on 2021-03-03 13:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0043_money_sum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='referrals_counts',
        ),
        migrations.AddField(
            model_name='profile',
            name='referrals_counts',
            field=models.ManyToManyField(blank=True, related_name='referrals_counts', to=settings.AUTH_USER_MODEL, verbose_name='Количество активных рефералов'),
        ),
    ]
