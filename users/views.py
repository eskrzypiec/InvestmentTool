from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, login, authenticate
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from .forms import *


class LoginUserView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "users/login.html"


class LogoutUserView(auth_views.LogoutView):
    template_name = 'users/logout.html'


class RegisterUserView(View):
    form_class = UserRegisterForm
    form_class_p = ProfileRegisterForm

    def get(self, request):
        form = self.form_class()
        form_p = self.form_class_p()
        return render(request, "users/register.html", {'form': form, 'form_p': form_p})

    def post(self, request):
        form = self.form_class(request.POST)
        form_p = self.form_class_p(request.POST)
        if form.is_valid() and form_p.is_valid():
            user = form.save()
            profile = form_p.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f'Konto dla {user.username} zostało utworzone')
            return redirect('login')
        return render(request, "users/register.html", {"form": form, "form_p": form_p})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'users/profile.html', {'p_form': p_form})

    def post(self, request):
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        button = request.POST.get('button')
        if button == 'update':
            if p_form.is_valid():
                p_form.save()
                messages.success(request, f'Twoje konto zostało zmodyfikowane')
                return redirect('profile')
            return render(request, 'users/profile.html', {'p_form': p_form})
        elif button == 'change_password':
            return redirect("change-password")


class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, "users/user_confirm_password_change.html", {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            auth_views.update_session_auth_hash(request, user)
            messages.success(request, "Hasło zostało zmienione")
            return redirect("profile")
        else:
            messages.error(request, "Prosze wprowadzić poprawne dane")
        return render(request, "users/user_confirm_password_change.html", locals())
