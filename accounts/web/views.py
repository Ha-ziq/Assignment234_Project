from django.shortcuts import redirect
from django.views.generic import TemplateView
from allauth.account.views import ConfirmEmailView
from django.contrib.auth import login

class EmailVerificationSentView(TemplateView):
    template_name = 'account/confirm_email.html'

# No longer needed unless you want to use it
# class EmailConfirmedView(TemplateView):
#     template_name = 'account/email_confirmed.html'

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        # Confirm the email using Allauth
        self.object = self.get_object()
        email_address = self.object.confirm(self.request)
        
        # Log in the user
        user = email_address.user
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Redirect to homepage or dashboard
        return redirect('/')  # Change to '/dashboard/' or another URL if needed
