from datetime import date, datetime, timedelta
from time import timezone

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from news.models import Post


def send_weekly_mails():
    global category, users_weekly_post_list
    weekly_post_list = Post.objects.filter(
        post_time_in__range=[datetime.now(timezone.utc) - timedelta(days=7), datetime.now(timezone.utc)])

    for user in User.objects.all():
        email = user.email
        for post in weekly_post_list:
            users_weekly_post_list = []

            category = [category[name] for category in post.categories.values('name') for name in category if
                        name == 'name']
            if user in post.subscribers_id_list():
                users_weekly_post_list.append(f'http://127.0.0.1:8000/news/{post.id}   ')

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, подписчик, {user.name}',
            body=f"Новые побликации за неделю ! {category}"
                 f" {users_weekly_post_list}   ",
            from_email='ayr215215@yandex.ru',
            to=email
        )
        if category:
            msg.send()
