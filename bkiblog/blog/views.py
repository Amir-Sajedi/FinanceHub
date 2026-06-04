from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import LoginForm,UserRegistrationForm
# Create your views here.


class MainPageView(TemplateView):
    template_name = "blog/main-page.html"


def user_login(request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(
                    request, username=data['username'], password=data['password']
                )
                if user is not None:
                        login(request, user)
                        return redirect('home')
                else:
                    form.add_error(None, 'Invalid Username or Password.')
        
        else:
            form = LoginForm()
    
        return render(request, 'blog/login.html', {'form':form})


def user_settings(request):
    return render(request, 'blog/settings.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'blog/register_done.html')
        
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'user_form': user_form })    


def custom_404(request, exception):
    return render(request, "404.html", status=404)