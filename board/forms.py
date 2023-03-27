from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Reply
from django.utils.translation import gettext_lazy as _
from markdownx.fields import MarkdownxFormField


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=255, label='Заголовок:')
    wysiwyn_text = MarkdownxFormField()

    class Meta:
        model = Post
        fields = [
                   'title',
                   'text',
                   'category',
                   'wysiwyn_text',
        ]
        labels = {'text': _('Текст'), 'category': _('Категория'), 'wysiwyn_text': _('Текст обьявления')
                 }

    def clean(self):
       cleaned_data = super().clean()
       text = cleaned_data.get("description")
       if text is not None and len(text) < 20:
           raise ValidationError({
               "text": "Статья/новость не может быть менее 20 символов."
           })

       # title = cleaned_data.get("title")
       # if len(title) > 255:
       #     raise ValidationError(
       #         "Заголовок не должно быть длиннее 255 символов."
       #     )

       return cleaned_data


class ReplyForm(forms.ModelForm):
    #reply_text = forms.CharField(max_length=255, label='Заголовок:')
    class Meta:
        model = Reply
        fields = [
                   'reply',
                 ]
        labels = {'reply': _('Отклик'),}

    def clean(self):
       cleaned_data = super().clean()
       # text = cleaned_data.get("description")
       # if text is not None and len(text) < 20:
       #     raise ValidationError({
       #         "text": "Статья/новость не может быть менее 20 символов."
       #     })

       # title = cleaned_data.get("title")
       # if len(title) > 255:
       #     raise ValidationError(
       #         "Заголовок не должно быть длиннее 255 символов."
       #     )

       return cleaned_data
