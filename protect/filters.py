import django_filters
from django_filters import FilterSet
from django.utils.translation import gettext_lazy as _
from board.models import Reply, Post


# Создаем свой набор фильтров для модели Post.
class ReplyFilter(FilterSet):
    class Meta:
        model = Post
        fields = ['title',]
        labels = {'title': _('Обьявление')}
    # class Meta:
    # В Meta классе мы должны указать Django модель,
    # в которой будем фильтровать записи.
    # model = Post
    # В fields мы описываем по каким полям модели
    # будет производиться фильтрация.
    # fields = {
    # поиск по названию
    # 'title': ['icontains'],
    # количество товаров должно быть больше или равно
    # 'author__user__username': ['icontains'],
    # }
