from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import news.signals

#       from .tasks import send_weekly_mails
#       from .scheduler import news_scheduler
#       print('started')

#       news_scheduler.add_job(
#           id='mail send',
#           func=send_weekly_mails,
#           trigger='interval',
#           seconds=10,
#       )
#       news_scheduler.start()
