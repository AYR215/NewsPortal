from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг всех комментариев к статьям автора.
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commRat = self.authorUser.comments_set.all().aggregate(commRating=Sum('rating'))
        cRat = 0
        cRat += commRat.get('commRating')

        post_author = self.post_set.all()
        sum_rating_comment_post_author = sum(
            [x['rating'] for x in Comments.objects.filter(comm_post__in=post_author).values()])

        self.author_rating = pRat * 3 + cRat + sum_rating_comment_post_author
        self.save()

    def __str__(self):
        return f'{self.authorUser.username}'


# class AuthorPosts(models.Model):
#    postThr = models.ForeignKey('Post', on_delete=models.CASCADE)
#    authorThr = models.ForeignKey(Author, on_delete=models.CASCADE)


class Category(models.Model):
    Business = 'BSN'
    Sport = 'SPR'
    Politics = 'PLT'
    Auto = 'AUT'

    CATEGORY = [(Business, 'Бизнес'),
                (Sport, 'Спорт'),
                (Politics, 'Политика'),
                (Auto, 'Авто'), ]

    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    ARTICLE = 'AT'
    NEWS = 'NW'

    TYPE = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    post_type = models.CharField(max_length=2, choices=TYPE, default=ARTICLE)
    post_time_in = models.DateTimeField(auto_now_add=True, verbose_name='(ММ/ДД/ГГГГ)Добавлено')
    categories = models.ManyToManyField(Category, through='PostCategory')
    headline = models.CharField(max_length=155, verbose_name='В заголовке')
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def subscriber_email_list(self):
        sub_user_email = []

        for cat in self.categories.values('id'):
            for subscribers in Category.objects.get(pk=int(cat['id'])).subscribers.values('id'):
                for email in User.objects.filter(pk=int(subscribers['id'])).values('email'):
                    sub_user_email.append(email['email'])
        return sub_user_email
    def subscribers_id_list(self):
        sub_user = []

        for cat in self.categories.values('id'):
            for subscribers in Category.objects.get(pk=int(cat['id'])).subscribers.values('id'):
                for user_id in User.objects.filter(pk=int(subscribers['id'])).values('id'):
                    sub_user.append(user_id['id'])
        return sub_user


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]} ...'

    def __str__(self):
        return f'{self.headline}{self.post_time_in}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    #def __str__(self):
    #    return f'{self.category.title()}'


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

    def __str__(self):
        return f'{self.comm_text()}'
