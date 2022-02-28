import redis
from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import news.signals


#red = redis.Redis(
#    host='redis-18178.c89.us-east-1-3.ec2.cloud.redislabs.com',
#    port=18178,
#    password='12oXXfgNWgdJqE8T72RVorQi7P6sC72x'
#)
