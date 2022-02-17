import form as form
import view as view
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, \
    DeleteView  # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post, Category, PostCategory
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm  # импортируем нашу форму


class PostDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'news_template/post_detail.html'
    context_object_name = 'postdetail'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        aaa = Category.objects.filter(pk=Post.objects.get(pk=id).post_categories.id).values("subscribers__username")
        context['is_not_subscribe'] = not aaa.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = aaa.filter(subscribers__username=self.request.user).exists()
        return context


# class NewsDetailView(DetailView):
#    template_name = 'news_detail.html'
#    queryset = Post.objects.all()
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        id = self.kwargs.get('pk')
#        aaa = Category.objects.filter(pk=Post.objects.get(pk=id).postCategory.name).values("subscribers__username")
#        context['is_not_subscribe'] = not aaa.filter(subscribers__username=self.request.user).exists()
#        context['is_subscribe'] = aaa.filter(subscribers__username=self.request.user).exists()
#        return context


# @login_required
def add_subscribe(request, pk, ):
    user = request.user
    sub_user = User.objects.get(id=user.pk)
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    print('Пользователь', user, 'добавлен в подписчики категории:', category_object_name)
    category_object_name.subscribers.add(sub_user)

    return redirect('/news/')


# функция отписки от группы
# @login_required
def del_subscribe(request, pk):
    user = request.user
    sub_user = User.objects.get(id=user.pk)
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    print('Пользователь', user, 'удален из подписчиков категории:', category_object_name)
    category_object_name.subscribers.remove(sub_user)
    return redirect('/news/')


class News(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-post_time_in')
    paginate_by = 10


# создаём представление, в котором будут детали конкретного отдельного поста
class NewsDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'newsdetail.html'  # название шаблона будет newsdetail.html
    context_object_name = 'newsdetail'  # название объекта. в нём будет


class Search(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'search'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
