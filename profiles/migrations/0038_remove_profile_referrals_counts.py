# Generated by Django 3.1.5 on 2021-03-02 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0037_profile_broker_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='referrals_counts',
        ),
    ]
