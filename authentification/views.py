from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from .forms import RegistrationForm, LoginForm

# Create your views here.

class LoginView(FormView):
    template_name = "authentification/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class RegisterView(FormView):
    template_name = "authentification/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        return redirect(self.success_url)


def logoutView(request):
    logout(request)
    return redirect('home')