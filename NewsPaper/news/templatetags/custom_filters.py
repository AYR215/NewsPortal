from django import template

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их
# искать и фильтры потеряются


@register.filter(name='Censor')
def Censor(value):
    test_list = ['дурак', 'идиот']
    for i in value.split():
        if i in test_list:
            value = value.replace(i, "!!!censored!!!")
    return value
