from django.forms import ModelForm, BooleanField  # Импортируем true-false поле
from .models import Post


class PostForm(ModelForm):
    check_box = BooleanField(label='Да')  # добавляем галочку, или же true-false поле

    class Meta:
        model = Post
        fields = ['headline', 'post_type', 'post_categories', 'text', 'author',
                  'check_box']  # не забываем включить галочку в поля иначе она не будет показываться на странице!