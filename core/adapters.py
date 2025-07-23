from allauth.account.adapter import DefaultAccountAdapter
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class CustomAccountAdapter(DefaultAccountAdapter):
  def send_password_reset_mail(self, request, user, context):
    print("=== Custom password reset mail function triggered ===")
    try:
        subject = render_to_string("account/email/password_reset_key_subject.txt", context).strip()
        body = render_to_string("account/email/password_reset_key_message.txt", context)

        # FIX: user is actually the email address string, so no `.email`
        msg = EmailMultiAlternatives(subject, body, None, [user])
        msg.send()
        print("✅ Password reset email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# from allauth.account.adapter import DefaultAccountAdapter
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string

# class CustomAccountAdapter(DefaultAccountAdapter):
#     def send_mail(self, template_prefix, email_template_context, to_email):
#         print("=== Custom password reset mail function triggered ===")
#         print(f"📩 Context (type: {type(email_template_context)}): {email_template_context}")
#         print(f"📨 To email: {to_email}")

#         # 🔁 Detect and auto-correct swapped params
#         if isinstance(to_email, dict) and isinstance(email_template_context, str):
#             print("⚠️ Detected swapped params, fixing...")
#             email_template_context, to_email = to_email, email_template_context
#             print("⚠️ Converted string context to dict as fallback")

#         try:
#             subject = render_to_string(f"{template_prefix}_subject.txt", email_template_context).strip()
#             body_txt = render_to_string(f"{template_prefix}_message.txt", email_template_context)

#             # Try loading HTML version
#             try:
#                 body_html = render_to_string(f"{template_prefix}_message.html", email_template_context)
#             except Exception as e:
#                 print(f"⚠️ HTML template load failed: {e}")
#                 body_html = None

#             msg = EmailMultiAlternatives(subject, body_txt, None, [to_email])
#             if body_html:
#                 msg.attach_alternative(body_html, "text/html")

#             msg.send()
#             print("✅ Email sent successfully!")

#         except Exception as e:
#             print(f"❌ Failed to send email: {e}")
