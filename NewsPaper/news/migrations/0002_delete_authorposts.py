# Generated by Django 4.0.1 on 2022-01-09 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AuthorPosts',
        ),
    ]
