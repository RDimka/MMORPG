from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
#import pytz #  импортируем стандартный модуль для работы с часовыми поясами
from django.shortcuts import redirect

from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy

from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404

from .models import Post, Category
#from .forms import PostForm
from .filters import PostFilter

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

class PostList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_time_in'

    template_name = 'news_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    context_object_name = 'news_list'
    paginate_by = 6

    # Переопределяем функцию получения списка статей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()

        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context



class PostDetail(DetailView):
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'news.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'


class PostSearchList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_time_in'

    template_name = 'news_search.html'

    context_object_name = 'news_list'
    paginate_by = 10

    # Переопределяем функцию получения списка статей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()

        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

# Добавляем новое представление для редактирования постов.
# class PostCreate(PermissionRequiredMixin, CreateView):
#
#     permission_required = ('news_app.add_post',)
#
#     # Указываем нашу разработанную форму
#     form_class = PostForm
#     # модель постов
#     model = Post
#     # и новый шаблон, в котором используется форма.
#     template_name = 'news_edit.html'
#
#     def form_valid(self, form):
#         post = form.save(commit=False)
#         path = self.request.META['PATH_INFO']
#
#         #сохраняем, чтобы получить id статьи
#         post = form.save()
#
#         # запускаем задачу на оповещение подписчиков о создании статьи
#         #notify_at_new_post_added.delay(post.pk)
#
#         return super().form_valid(form)

# class PostUpdate(PermissionRequiredMixin, UpdateView):
#
#     permission_required = ('news_app.change_post',)
#
#     form_class = PostForm
#     model = Post
#     template_name = 'news_edit.html'


# Представление удаляющее товар.
# class PostDelete(DeleteView):
#     model = Post
#     template_name = 'news_delete.html'
#     success_url = reverse_lazy('news_list')


# class CategoryList(ListView):
#     model = Post
#     template_name = 'category_list.html'
#     context_object_name = 'category_post_list'
#
#     def get_queryset(self):
#         #Получим одну категорию по pk из url
#         self.category = get_object_or_404(Category, id=self.kwargs['pk'])
#
#         #Список статей, принадлежащих данной категории
#         post_list_by_category = Post.objects.filter(category=self.category).order_by('-date_time_in')
#
#         return post_list_by_category
#
#     #проверяем подписан ли User на эту категорию
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         #Добавляем флаг если не пользователь
#         context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
#         context['category'] = self.category
#         return context

#только для зареганных пользователей
# @login_required
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#
#     message = "Вы подписались на рссылку новостей категории "
#     return render(request, 'subscribe.html', {'category': category, 'message': message})