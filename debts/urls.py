from django.urls import path
from .views import *

urlpatterns = [
    path("", login, name="login"),
    path('loans/', LoanListView.as_view(), name='loan_list'),
    path('loan/create/', CreateLoanView.as_view(), name='create_loan'),
    path('loan/<int:loan_id>/', LoanDetailView.as_view(), name='loan_detail'),
    path('loan/<int:loan_id>/make_payment/', MakePaymentView.as_view(), name='make_payment'),
    path('loan/<int:pk>/edit/', LoanUpdateView.as_view(), name='loan_update'),
    path('loan/<int:pk>/delete/', LoanDeleteView.as_view(), name='loan_delete'),
    path('payment/<int:pk>/edit/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payment/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),
    path('<int:loan_id>/send_notification/', SendLoanNotificationView.as_view(), name='send_loan_notification'),
 ]
