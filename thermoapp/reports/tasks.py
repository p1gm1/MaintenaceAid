# Django
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Celery
from config import celery_app

# Models
from thermoapp.users.models import User
from thermoapp.reports.models import Component, BasePhoto

@celery_app.task(name='send_fail_email')
def send_fail_email(user_pk, component_pk, photo_pk):
    """Send notification email, in case
    of a bad photo.
    """

    user = User.objects.get(pk=user_pk)
    component = Component.objects.get(pk=component_pk)
    photo = BasePhoto.objects.get(pk=photo_pk)

    subject = f'{user.username}, revision termografias'
    from_email = 'Thermoapp <noreply@thermoapp.com>'
    to = user.email
    content = render_to_string(
        'account/photo_mail_send.html',
        context = {
            'user': user,
            'component': component,
            'photo': photo
        }
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=content,
        from_email=from_email,
        to=[to]
    )
    msg.attach_alternative(content, "text/html")
    msg.send()

