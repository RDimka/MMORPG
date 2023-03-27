import datetime
from random import randint, seed

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView

from MMORPG import settings
from .forms import RegistrationForm, MyActivationCodeForm
from .models import BaseRegisterForm, Profile

from django.contrib.auth.decorators import login_required


def generate_code():
    seed()
    return str(randint(10000, 99999))


def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password1 = form.cleaned_data.get('password1')
                u_f = User.objects.get(username=username, email=email, is_active=False)

                #группа Author
                author_group = Group.objects.get(name='Author')
                author_group.user_set.add(u_f)

                code = generate_code()
                if Profile.objects.filter(code=code):
                    # for p in Profile.objects.filter(code=code):
                    #     p.delete()
                    code = generate_code()

                message = code
                user = authenticate(username=username, password=my_password1)
                now = datetime.datetime.now()

                Profile.objects.create(user=u_f, code=code, date=now)

                send_mail('код подтверждения',
                          message,
                          settings.DEFAULT_FROM_EMAIL,
                          [email],
                          fail_silently=False)

                if user and user.is_active:
                    login(request, user)
                    return redirect('/personalArea/')
                else:  # тут добавить редирект на страницу с формой для ввода кода.
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('../activation_code_form')
                    # return render(request, 'registration/register.html', {'form': form})

            else:
                return render(request, 'sign/register.html', {'form': form})
        else:
            return render(request, 'sign/register.html', {'form': RegistrationForm()})
    else:
        return redirect('/personalArea/')


def endreg(request):
    if request.user.is_authenticated:
        return redirect('/personalArea/')
    else:
        if request.method == 'POST':
            print('Зашли в POST')
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                print('форма валидна')
                code_use = form.cleaned_data.get("code")
                if Profile.objects.filter(code=code_use):
                    print('есть такой код')
                    profile = Profile.objects.get(code=code_use)
                    print(profile)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'sign/activation_code_form.html', {'form': form})
                if profile.user.is_active == False:
                    profile.user.is_active = True
                    profile.user.save()
                    print('Активировали аккаунт')
                    print(profile.user.username)
                    print(profile.user.password)
                    user = authenticate(request, username=profile.user.username, password=profile.user.password)
                    print(user)
                    if user is not None:
                        print('Юзера действительно авторизовали')
                        login(request, user)
                        print('залогинили')
                        # login(request, profile.user)
                    else:
                        print('Юзер не был авторизован')
                    profile.delete()
                    #переходим на страницу входа
                    return redirect('/sign/login')
                else:
                    print ('Пользователь уже активирован')
                    form.add_error(None, 'Unknown or disabled account')
                return render(request, 'sign/activation_code_form.html', {'form': form})
            else:
                print('Форма не валидна')
                return render(request, 'sign/activation_code_form.html', {'form': form})
        else:
            print('запрос GET')
            form = MyActivationCodeForm()
            return render(request, 'sign/activation_code_form.html', {'form': form})


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')
