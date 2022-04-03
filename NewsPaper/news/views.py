from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .tasks import send_weekly_mails
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm  # импортируем нашу форму
from .models import Post, Category, PostCategory
from django.core.cache import cache  # импортируем наш кэш


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news_template/post_detail.html'
    context_object_name = 'postdetail'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


@login_required
def subscribe_me(request, news_category_id):
    user = request.user
    my_category = Category.objects.get(id=news_category_id)
    sub_user = User.objects.get(id=user.pk)
    if my_category.subscribers.filter(id=user.pk):
        my_category.subscribers.remove(sub_user)
        return redirect(f'/news/')
    else:
        my_category.subscribers.add(sub_user)
        return redirect(f'/news/')


class News(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции
    # о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-post_time_in')
    paginate_by = 10


class CategoryBusinessNews(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'business_news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции
    # о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'businessnews'  # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.all().filter(categories=1)
    paginate_by = 10


class CategorySportNews(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'sport_news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции
    # о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'sportnews'  # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.all().filter(categories=2)
    paginate_by = 10


class CategoryPoliticNews(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'politic_news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции
    # о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'politicnews'  # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.all().filter(categories=3)
    paginate_by = 10


class CategoryAutoNews(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'auto_news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции
    # о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'autonews'  # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.all().filter(categories=4)
    paginate_by = 10


class Search(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все
    # инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'search'  # это имя списка, в котором будут лежать все объекты, его надо указать,

    # чтобы обратиться к самому списку объектов через HTML-шаблон

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


#@receiver(m2m_changed, sender=PostCategory)
#def send_sub_mail(sender, instance, **kwargs):
#   emailadress = instance.subscriber_email_list()
#
#   category = [category[name] for category in instance.categories.values('name') for name in category if
#               name == 'name']
#
#   msg = EmailMultiAlternatives(
#       subject=f'Здравствуй, подписчик!',
#       body=f"Новая статья в вашем разделе! {category}"
#            f" 'http://127.0.0.1:8000/news/{instance.id}'"
#            f"'{instance.text[:20]}'     {instance.author}   ",
#       from_email='ayr215215@yandex.ru',
#       to=emailadress
#   )
#   if category:
#       msg.send()
#   #print(emailadress)
#
#def send_weekly_mails():
#   global category, users_weekly_post_list
#   weekly_post_list = Post.objects.filter(
#       post_time_in__range=(datetime.now() - timedelta(days=7), datetime.now()))
#
#   for user in User.objects.all():
#       email = user.email
#       for post in weekly_post_list:
#           users_weekly_post_list = []
#
#           category = [category[name] for category in post.categories.values('name') for name in category if
#                       name == 'name']
#           if user in post.subscribers_id_list():
#               users_weekly_post_list.append(f'http://127.0.0.1:8000/news/{post.id}   ')
#
#       msg = EmailMultiAlternatives(
#           subject=f'Здравствуй, подписчик, {user.name}',
#           body=f"Новые побликации за неделю ! {category}"
#                f" {users_weekly_post_list}   ",
#           from_email='ayr215215@yandex.ru',
#           to=email
#       )
#       if category:
#           msg.send()


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся
    # редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


def week_digest():
    send_weekly_mails.delay()


week_digest()
