# Generated by Django 4.2.16 on 2024-11-17 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='repayment_schedule',
        ),
    ]