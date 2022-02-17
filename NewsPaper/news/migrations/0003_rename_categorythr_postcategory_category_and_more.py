# Generated by Django 4.0.1 on 2022-02-04 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_delete_authorposts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcategory',
            old_name='categoryThr',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='postcategory',
            old_name='postThr',
            new_name='post',
        ),
        migrations.AlterField(
            model_name='post',
            name='headline',
            field=models.CharField(max_length=155, verbose_name='В заголовке'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_time_in',
            field=models.DateTimeField(auto_now_add=True, verbose_name='(ММ/ДД/ГГГГ)Добавлено'),
        ),
    ]
