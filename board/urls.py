from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail#, PostSearchList, PostCreate

from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', PostList.as_view(), name='news_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='news_detail'),
   # path('index', Index.as_view(), name='index'),
   # path('search', PostSearchList.as_view(), name='news_search'),
   # path('news/create/', PostCreate.as_view(), name='news_create'),
   # path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
   # path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   # path('article/create/', PostCreate.as_view(), name='article_create'),
   # path('article/<int:pk>/update', PostUpdate.as_view(), name='article_update'),
   # path('article/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
   #
   # path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
   # path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]