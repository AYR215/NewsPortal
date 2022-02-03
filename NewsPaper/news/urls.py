from django.urls import path
from .views import News, NewsDetail, Search  # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем новостям у нас останется пустым, позже станет ясно, почему
    path('', News.as_view()),
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', NewsDetail.as_view()),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('search', Search.as_view()),
]