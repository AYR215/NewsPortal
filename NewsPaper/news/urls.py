from django.urls import path
from .views import News, Search, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, \
    subscribe_me, CategoryAutoNews, CategoryBusinessNews, CategorySportNews, CategoryPoliticNews
# импортируем наше представление
from django.views.decorators.cache import cache_page



urlpatterns = [
    # path — означает путь. В данном случае путь ко всем новостям у нас останется пустым, позже станет ясно, почему
    path('', cache_page(60*5)(News.as_view())),
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    # path('<int:pk>', PostDetailView.as_view()),  # pk — это первичный ключ поста, который будет выводиться у нас в
    # шаблон
    path('search', Search.as_view()),
    path('add', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание поста
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),  # Ссылка на детали поста
    path('category/1', cache_page(60*5)(CategoryBusinessNews.as_view()), name='business_news'),
    path('category/2', cache_page(60*5)(CategorySportNews.as_view()), name='sport_news'),
    path('category/3', cache_page(60*5)(CategoryPoliticNews.as_view()), name='politic_news'),
    path('category/4', cache_page(60*5)(CategoryAutoNews.as_view()), name='auto_news'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('subscribed/<int:news_category_id>', subscribe_me, name='subscribed'),
]
