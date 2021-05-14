from django.core.mail import send_mail


def send_activation_email(user):
    subject = 'Thank you for the registration!'
    body = 'Thanks for the registration on our site!\n'\
        'For activation an account follow link bellow:\n'\
            f'http://127.0.0.1:8000/v1/account/activate/{user.activation_code}/'
    from_email = 'e-shop@django.kg'
    recipients = [user.email]
    send_mail(subject=subject, message=body, from_email=from_email, recipient_list=recipients, fail_silently=False)