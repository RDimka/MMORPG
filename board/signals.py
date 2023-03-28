from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from MMORPG import settings
from board.models import Reply


def send_email_notif(reply, title, template, subscribers_email):
    #берет за основу шаблон и создает текст письма
    html_mail = render_to_string(
        template,
        {
            'text': reply,
        }
    )

    message = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email
    )

    message.attach_alternative(html_mail, 'text/html')
    message.send()


@receiver(post_save, sender=Reply)
def new_reply_added(sender, instance, **kwargs):
    #print('Сработал сигнал по добавлению отклика')
    #событие - добавление отклика
    if kwargs['created'] == True:
        send_email_notif(instance.reply, f'Новый отклик на обьявление {instance.post.title}', 'reply_add_email.html', [instance.user.email])

@receiver(post_save, sender=Reply)
def reply_accepted(sender, instance, **kwargs):
    #print('Сработал сигнал по сохранению отклика')
    #событие - добавление отклика
    if kwargs['update_fields'] == {'accepted'}:
        send_email_notif(instance.reply, f'Ваш отклик принят. Обьявление: {instance.post.title}', 'reply_accepted_email.html', [instance.user.email])