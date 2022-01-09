from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        #суммарный рейтинг всех комментариев к статьям автора.
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commRat = self.authorUser.comments_set.all().aggregate(commRating=Sum('rating'))
        cRat = 0
        cRat += commRat.get('commRating')

        post_author = self.post_set.all()
        sum_rating_comment_post_author = sum([x['rating'] for x in Comments.objects.filter(comm_post__in=post_author).values()])

        self.author_rating = pRat*3 + cRat + sum_rating_comment_post_author
        self.save()


#class AuthorPosts(models.Model):
#    postThr = models.ForeignKey('Post', on_delete=models.CASCADE)
#    authorThr = models.ForeignKey(Author, on_delete=models.CASCADE)


class Category(models.Model):

    name = models.CharField(max_length=64,
                            unique=True)


class Post(models.Model):
    ARTICLE = 'AT'
    NEWS = 'NW'

    TYPE = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    post_type = models.CharField(max_length=2,choices=TYPE, default=ARTICLE)
    post_time_in = models.DateTimeField(auto_now_add=True)
    post_categories = models.ManyToManyField(Category, through='PostCategory')
    headline = models.CharField(max_length=155)
    text =  models.TextField()
    rating = models.SmallIntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]} ...'
        

class PostCategory(models.Model):
    postThr = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThr = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comments(models.Model):
    comm_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comm_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comm_text = models.TextField()
    comm_time_in = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


#Создать двух пользователей (с помощью метода User.objects.create_user('username')).
#Создать два объекта модели Author, связанные с пользователями.
#Добавить 4 категории в модель Category.
#Добавить 2 статьи и 1 новость.
#Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
#Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
#Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
#Обновить рейтинги пользователей.
#Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
#Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
#Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.