from django.shortcuts import render
from django.contrib.auth import views as auth_views, login, authenticate
from django.views import View


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
            send_registration_mail(user.email)
            #tu wysylamy maila z potwierdzeniem
            messages.success(request, f'Konto dla {user.username} zostało utworzone')
            return redirect('login')
        return render(request, "users/register.html", {"form": form, "form_p": form_p})

