from django.urls import path
from .views import IndexView
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='reply_list'),
    path('protect/accept/<int:pk>', views.accept_reply, name="accept_reply"),
    #path('filter/<int:pk>', PostDetail.as_view(), name='news_detail'),
]