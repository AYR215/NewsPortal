from datetime import date, datetime, timedelta
from time import timezone
from celery.app import task
from django.utils.timezone import utc
from django.core.mail import EmailMultiAlternatives
from celery import shared_task, app
from .models import Post
from django.contrib.auth.models import User


# from django_celery_beat.models import PeriodicTask


@shared_task
def send_weekly_mails():
    print("Посты за неделю")
    global category, users_weekly_post_list
    weekly_post_list = Post.objects.filter(
        post_time_in__range=[datetime.now() - timedelta(days=7), datetime.now()])

    for user in User.objects.all():
        email = [user.email, ]
        users_weekly_post_list = []
        for post in weekly_post_list:
            category = [category[name] for category in post.categories.values('name') for name in category if
                        name == 'name']
            if user.id in post.subscribers_id_list():
                users_weekly_post_list.append(f'http://127.0.0.1:8000/news/{post.id}    в категории {category}.')

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, подписчик, {user.username}',
            body=f"Новые публикации за неделю ! "
                 f" {users_weekly_post_list}   ",
            from_email='ayr215215@yandex.ru',
            to=email
        )
        if users_weekly_post_list:
            msg.send()
    #print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")



