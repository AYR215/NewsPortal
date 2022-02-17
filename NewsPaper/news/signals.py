from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post


# создаём функцию обработчик с параметрами под регистрацию сигнала
@receiver(post_save, sender=Post)
def notify_users_mailing(sender, instance, created, **kwargs):
    subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )