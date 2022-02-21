from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.utils.timezone import utc

from .models import Post, PostCategory

import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import date, datetime, timedelta
from time import timezone

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from .models import Post


# создаём функцию обработчик с параметрами под регистрацию сигнала
@receiver(m2m_changed, sender=PostCategory)
def send_sub_mail(sender, instance, **kwargs):
    emailadress = instance.subscriber_email_list()

    category = [category[name] for category in instance.categories.values('name') for name in category if
                name == 'name']

    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, подписчик!',
        body=f"Новая статья в вашем разделе! {category}"
             f" 'http://127.0.0.1:8000/news/{instance.id}   '"
             f"'{instance.text[:20]}'     {instance.author}   ",
        from_email='ayr215215@yandex.ru',
        to=emailadress
    )
    if category:
        msg.send()
    # print(emailadress)

