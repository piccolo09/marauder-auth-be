# Generated by Django 3.2.7 on 2021-10-11 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211009_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='activated',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email_confirmed',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='setup_completed',
        ),
    ]
