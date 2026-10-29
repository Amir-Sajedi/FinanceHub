import logging

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from conversionapp.services import get_market_rates

from .forms import LoginForm, UserRegistrationForm

logger = logging.getLogger(__name__)


class MainPageView(TemplateView):
    template_name = "blog/main-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            market_rates, market_is_live = get_market_rates(timeout=4)
        except Exception as exc:  # صفحه اصلی هرگز نباید خطا بدهد
            logger.warning('Home market rates unavailable: %s', exc)
            market_rates, market_is_live = {}, False
        context['market_rates'] = market_rates
        context['market_is_live'] = market_is_live
        context['market_available'] = bool(market_rates)
        return context


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = LoginForm(request)

    return render(request, 'blog/login.html', {'form': form})


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
