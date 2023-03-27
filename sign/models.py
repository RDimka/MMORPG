from django.db import models

from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
#from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django import forms

from django.core.mail import send_mail

class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile', default=None, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateField(blank=True, null=True)


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        #basic_group = Group.objects.get(name='common')
        #basic_group.user_set.add(user)

        # send_mail(
        #     'Вы зарегистрировались MMORPG',
        #     'Поздравляю, вы успешно прошли регистрацию на MMORPG',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[user.email, ]
        # )

        return user