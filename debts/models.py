from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.username


class Loan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('paid', 'Оплачено'),
        ('overdue', 'Просрочено'),
    ]
    lender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lender_loans')  
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='borrower_loans')  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) 
    loan_date = models.DateTimeField(auto_now_add=True)  
    due_date = models.DateTimeField()  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"Заем от {self.lender.username} к {self.borrower.username} на сумму {self.amount}"


class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    payer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments_made') 
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    payment_date = models.DateTimeField(auto_now_add=True) 
    payment_method = models.CharField(max_length=50)  
    status = models.CharField(max_length=20, choices=[('success', 'Успешно'), ('failed', 'Неудачно')], default='success')

    def __str__(self):
        return f"Платеж {self.amount} для займа {self.loan.id}"



class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallets')  
    currency = models.CharField(max_length=3, choices=[('RUB', 'RUB'), ('USD', 'USD')])  
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Кошелек {self.currency} пользователя {self.user.username}"
