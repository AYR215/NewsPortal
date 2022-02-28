from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives


from .models import Post, PostCategory
from django.core.mail import EmailMultiAlternatives




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

