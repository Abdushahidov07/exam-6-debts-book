# Generated by Django 4.2.16 on 2024-11-18 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0002_remove_loan_repayment_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanhistory',
            name='loan',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='loan',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.DeleteModel(
            name='SystemSetting',
        ),
        migrations.DeleteModel(
            name='LoanHistory',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]