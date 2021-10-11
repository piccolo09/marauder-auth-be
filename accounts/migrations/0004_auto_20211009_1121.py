# Generated by Django 3.2.7 on 2021-10-09 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211009_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activated',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Account Activated'),
        ),
        migrations.AddField(
            model_name='user',
            name='email_confirmed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Email Confirmed'),
        ),
        migrations.AddField(
            model_name='user',
            name='setup_completed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Setup Complete'),
        ),
    ]