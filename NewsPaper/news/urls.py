from django.urls import path
from .views import News, Search, NewsDetail, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, \
     subscribe_me

# импортируем наше представление


urlpatterns = [
    # path — означает путь. В данном случае путь ко всем новостям у нас останется пустым, позже станет ясно, почему
    path('', News.as_view()),
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    # path('<int:pk>', PostDetailView.as_view()),  # pk — это первичный ключ поста, который будет выводиться у нас в
    # шаблон
    path('search', Search.as_view()),
    path('add', PostCreateView.as_view()),  # Ссылка на создание поста
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),  # Ссылка на детали поста

    path('<int:pk>/edit', PostUpdateView.as_view()),
    path('<int:pk>/delete', PostDeleteView.as_view()),
    path('subscribed/<int:news_category_id>', subscribe_me, name='subscribed'),
]
