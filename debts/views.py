from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import *
from django.utils import timezone
from .models import Loan, Payment
from .forms import PaymentForm
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse


class LoanListView(ListView):
    model = Loan
    template_name = 'loan_list.html'
    context_object_name = 'loans'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Loan.objects.all()
        
        return Loan.objects.filter(
            Q(borrower=self.request.user) | Q(lender=self.request.user)
        )


class CreateLoanView(CreateView):
    model = Loan
    template_name = 'create_loan.html'
    fields = ['borrower', 'amount', 'interest_rate', 'due_date']
    
    def form_valid(self, form):
        loan = form.save(commit=False)
        loan.lender = self.request.user
        loan.remaining_amount = loan.amount
        loan.status = 'active'
        loan.save()
        return redirect('loan_detail', loan_id=loan.id)


class LoanDetailView(DetailView):
    model = Loan
    template_name = 'loan_detail.html'
    context_object_name = 'loan'

    def get_object(self):
        loan_id = self.kwargs['loan_id']
        loan = get_object_or_404(Loan, id=loan_id)

        if not self.request.user.is_staff:
            if loan.lender != self.request.user and loan.borrower != self.request.user:
                raise PermissionDenied("У вас нет доступа к этому займу.")
        
        # Отправить уведомление, если это заем для заемщика
        if loan.borrower == self.request.user and not self.request.user.is_staff:
            self.send_loan_notification(loan)  

        return loan

    def send_loan_notification(self, loan):
        subject = f"Уведомление о текущем долге по займу №{loan.id}"
        message = f"Здравствуйте, {loan.lender.username}!\n\n" \
                  f"Сумма вашего долга по займу №{loan.id} составляет {loan.remaining_amount}\n" \
                  f"Пожалуйста, ознакомьтесь с деталями займа и совершите необходимые платежи.\n\n" \
                  f"Дата займа: {loan.loan_date.strftime('%Y-%m-%d')}\n" \
                  f"Дата возврата: {loan.due_date.strftime('%Y-%m-%d')}\n" \
                  f"Процентная ставка: {loan.interest_rate}%\n\n" \
                  f"С уважением, ваша компания."
        
        recipient_list = [loan.lender.email]
        print(loan.lender.email)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list
        )


class SendLoanNotificationView(View):
    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id)

        if not request.user.is_staff:
            raise PermissionDenied("Только администратор может отправлять уведомления.")

        loan_detail_view = LoanDetailView()
        loan_detail_view.send_loan_notification(loan)

        return HttpResponse("Уведомление отправлено на email!", status=200)


def login(request):
    return redirect("accounts/login")


class MakePaymentView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'make_payment.html'

    def form_valid(self, form):
        loan = get_object_or_404(Loan, id=self.kwargs['loan_id'])
        payment = form.save(commit=False)
        payment.loan = loan
        payment.payer = self.request.user
        payment.status = 'success'
        payment.payment_date = timezone.now()

        if loan.lender != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied

        payment.save()
        
        loan.remaining_amount -= payment.amount
        if loan.remaining_amount <= 0:
            loan.status = 'paid'
        loan.save()

        return redirect('loan_detail', loan_id=loan.id)


class LoanUpdateView(UpdateView):
    model = Loan
    fields = ['borrower', 'amount', 'interest_rate', "status", 'due_date']
    template_name = 'loan_update.html'

    def get_success_url(self):
        return reverse_lazy('loan_detail', kwargs={'loan_id': self.object.id})

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_staff:
            raise PermissionDenied("Только администратор может редактировать этот объект.")
        return obj


class LoanDeleteView(DeleteView):
    model = Loan
    template_name = 'loan_confirm_delete.html'
    success_url = reverse_lazy('loan_list')

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_staff:
            raise PermissionDenied("Только администратор может удалить этот объект.")
        return obj


class PaymentUpdateView(UpdateView):
    model = Payment
    fields = ['amount', 'payment_method', 'status']
    template_name = 'payment_update.html'

    def get_success_url(self):
        return reverse_lazy('loan_detail', kwargs={'loan_id': self.object.loan.id})

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_staff:
            raise PermissionDenied("Только администратор может редактировать этот объект.")
        return obj


class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'payment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('loan_detail', kwargs={'loan_id': self.object.loan.id})

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_staff:
            raise PermissionDenied("Только администратор может удалить этот объект.")
        return obj
