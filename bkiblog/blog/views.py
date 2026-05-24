from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import LoginForm
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
        form = LoginForm()
    
    return render(request, 'blog/login.html', {'form':form})


def user_settings(request):
    return render(request, 'blog/settings.html')
