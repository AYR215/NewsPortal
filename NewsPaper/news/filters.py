from django_filters import FilterSet, CharFilter, DateFilter, ModelMultipleChoiceFilter
from .models import Post
from django.forms import DateInput
from .models import Author, Category, Post, PostCategory, Comments


# создаём фильтр
class PostFilter(FilterSet):
    author = CharFilter(
        field_name='author_id__authorUser_id__username',
        lookup_expr='icontains',
        label='Автор'
    )

    headline = CharFilter(
        field_name='headline',
        lookup_expr='icontains',
        label='Заголовок'
    )

    post_time_in = DateFilter(
        field_name='post_time_in',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Позже даты'
    )

    class Meta:
        model = Post
        fields = []