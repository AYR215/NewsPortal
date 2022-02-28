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

from NewsPaper.news.models import Post

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран

def send_weekly_mails():
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_weekly_mails,
            trigger=CronTrigger(day="*/7"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="send_weekly_mails",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_mails'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
