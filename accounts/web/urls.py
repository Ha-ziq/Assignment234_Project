from django.urls import path, include
from .views import (
    EmailVerificationSentView,
    CustomConfirmEmailView
)

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/email-verification-sent/', EmailVerificationSentView.as_view(), name='account_email_verification_sent'),
    path('accounts/confirm-email/<key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    # 🚫 Remove this line:
    # path('accounts/email-confirmed/', EmailConfirmedView.as_view(), name='account_email_confirmed'),
]
