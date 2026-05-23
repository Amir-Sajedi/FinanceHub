from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import scraper

# Create your views here.


class ConversionViewView(LoginRequiredMixin, TemplateView):
    
    template_name = 'conversionapp/converter.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Universal Converter'
       
       
        try:
            exchange_data = scraper.scrape_market_prices()
            context['exchange_rates'] = exchange_data
      
        except Exception as e:
            context['exchange_rates'] = {}
            context['error_message'] = "Unable to fetch exchange rates"
        
        return context