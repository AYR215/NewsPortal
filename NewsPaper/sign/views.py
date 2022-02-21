from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from .models import BaseRegisterForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.apps import apps





class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'





@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    author = apps.get_model('news', 'Author')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        author.objects.create(authorUser_id=user.pk)

    return redirect('/')