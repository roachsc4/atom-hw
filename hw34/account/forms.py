from django import forms
from . import models
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.core.urlresolvers import reverse_lazy
# login Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.

from .models import User

class UserCreationFormCustom(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    age = forms.IntegerField(min_value=0)

    class Meta:
        model = models.User
        fields = '__all__'#("username", "email", "first_name", "last_name", "age" )
        #field_classes = {'username': UsernameField}


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "account/login.html"

    # В случае успеха перенаправим на главную.
    success_url = reverse_lazy('roadmap:roadmaps')

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class RegisterFormView(FormView):
    form_class = UserCreationFormCustom  #Переопределить!!!!

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = reverse_lazy('account:login')

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "account/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")