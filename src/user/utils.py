from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def email_new_registration(user):
    """Send email for new registration"""

    subject = f'Welcome {user.name}'
    message = render_to_string(
        'emails/new_registration.html',
        {'user_name': user.name}
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send()


def email_forget_password(user, token):
    """Send email for password reset after forget password."""

    subject = 'Password Reset Request'
    reset_url = f"{settings.FRONTEND_URL}/api/user/reset-password/{token}/"
    message = render_to_string(
        'emails/password_reset_email.html',
        {'reset_url': reset_url, 'user_name': user.name}
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send()

def email_password_reset_success(user):
    """Send email for password reset successful."""

    subject = 'Password Reset successful'
    message = render_to_string(
        'emails/password_reset_successful.html',
        {'user_name': user.name}
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send()

def email_password_change_success(user):
    """Send email for password change successful."""

    subject = 'Password Change successful.'
    message = render_to_string(
        'emails/password_change_successful.html',
        {'user_name': user.name}
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    email = EmailMessage(subject, message, from_email, recipient_list)

    email.content_subtype = 'html'
    email.send()
