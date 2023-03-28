from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import ReplyFilter
from board.models import Reply


class IndexView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'protect/index.html'
    context_object_name = 'reply_list'
    ordering = '-date_time_in'
    paginate_by = 6

    # Переопределяем функцию получения списка откликов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()

        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ReplyFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

@login_required
def accept_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    if reply:
        reply.accepted = True
        reply.save(update_fields=['accepted'])
    return redirect('/')
