import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
app = Celery('NewsPaper')
app.autodiscover_tasks()
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379'

app.conf.beat_schedule = {
    'action_every_monday_at_8_am': {
        'task': 'news.tasks.send_weekly_mails',
        'schedule': crontab(minute='0', hour='8', day_of_week='mon'),
    },
}
#hour=8, minute=0, day_of_week='thursday'