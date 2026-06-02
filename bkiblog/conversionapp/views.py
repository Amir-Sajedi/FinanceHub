from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .scraper import scrape_market_prices, PriceScraperError

# Create your views here.


class ConversionViewView(LoginRequiredMixin, TemplateView):
    
    template_name = 'conversionapp/converter.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Universal Converter'
       
        try:
            # Fetch live market prices
            raw_data = scrape_market_prices()
            
            # Format data for template (convert flat structure to nested with price key)
            exchange_rates = {}
            
            if 'gold_18k' in raw_data:
                exchange_rates['gold_18k'] = {'price': raw_data['gold_18k']}
            if 'gold_24k' in raw_data:
                exchange_rates['gold_24k'] = {'price': raw_data['gold_24k']}
            if 'gold_oz' in raw_data:
                exchange_rates['gold_oz'] = {'price': raw_data['gold_oz']}
            if 'silver_gram' in raw_data:
                exchange_rates['silver_gram'] = {'price': raw_data['silver_gram']}
            if 'silver_oz' in raw_data:
                exchange_rates['silver_oz'] = {'price': raw_data['silver_oz']}
            if 'usd' in raw_data:
                exchange_rates['usd'] = raw_data['usd']
            
            context['exchange_rates'] = exchange_rates
            
        except (PriceScraperError, Exception) as e:
            context['exchange_rates'] = {}
            context['error_message'] = f"Unable to fetch live exchange rates: {str(e)}"
        
        return context


class NetWorthView(LoginRequiredMixin, TemplateView):
    template_name = 'conversionapp/networth.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Net Worth Tracker'
        
        from .models import UserHolding, NetWorthHistory
        from django.db.models import Sum
        
        try:
            # Fetch live market prices
            raw_data = scrape_market_prices()
            
            # Format exchange rates
            exchange_rates = {}
            if 'gold_18k' in raw_data:
                exchange_rates['gold_18k'] = {'price': raw_data['gold_18k']}
            if 'gold_24k' in raw_data:
                exchange_rates['gold_24k'] = {'price': raw_data['gold_24k']}
            if 'usd' in raw_data:
                exchange_rates['usd'] = raw_data['usd']
            
            context['exchange_rates'] = exchange_rates
            
            # Get or create user holdings
            holdings, created = UserHolding.objects.get_or_create(user=self.request.user)
            context['holdings'] = holdings
            
            # Calculate current net worth using live rates
            if all(k in raw_data for k in ['gold_18k', 'gold_24k', 'usd']):
                net_worth = holdings.calculate_net_worth(
                    raw_data['gold_18k'],
                    raw_data['gold_24k'],
                    raw_data['usd']
                )
                context['net_worth'] = net_worth
                
                # Calculate breakdown values
                context['gold18_value'] = float(holdings.gold18) * raw_data['gold_18k']
                context['gold24_value'] = float(holdings.gold24) * raw_data['gold_24k']
                context['usd_value'] = float(holdings.usd) * raw_data['usd']
            else:
                context['net_worth'] = 0
                context['gold18_value'] = 0
                context['gold24_value'] = 0
                context['usd_value'] = 0
            
            # Get net worth history for chart (last 30 days)
            from django.utils import timezone
            from datetime import timedelta
            
            thirty_days_ago = timezone.now() - timedelta(days=30)
            history = NetWorthHistory.objects.filter(
                user=self.request.user,
                timestamp__gte=thirty_days_ago
            ).order_by('timestamp')
            
            # Prepare chart data
            chart_data = {
                'labels': [h.timestamp.strftime('%Y-%m-%d') for h in history],
                'values': [float(h.net_worth) for h in history]
            }
            context['chart_data'] = chart_data
            context['history_count'] = history.count()
            
        except (PriceScraperError, Exception) as e:
            context['exchange_rates'] = {}
            context['error_message'] = f"Unable to fetch live exchange rates: {str(e)}"
            context['net_worth'] = 0
            context['chart_data'] = {'labels': [], 'values': []}
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle holding updates and snapshot creation"""
        from .models import UserHolding, NetWorthHistory
        from django.http import JsonResponse
        from decimal import Decimal, InvalidOperation
        
        action = request.POST.get('action')
        
        if action == 'update_holdings':
            try:
                holdings, created = UserHolding.objects.get_or_create(user=request.user)
                
                # Update holdings
                holdings.gold18 = Decimal(request.POST.get('gold18', 0))
                holdings.gold24 = Decimal(request.POST.get('gold24', 0))
                holdings.usd = Decimal(request.POST.get('usd', 0))
                holdings.save()
                
                return JsonResponse({'status': 'success', 'message': 'Holdings updated successfully'})
            except (InvalidOperation, ValueError) as e:
                return JsonResponse({'status': 'error', 'message': f'Invalid input: {str(e)}'}, status=400)
        
        elif action == 'save_snapshot':
            try:
                # Fetch live rates
                raw_data = scrape_market_prices()
                holdings, created = UserHolding.objects.get_or_create(user=request.user)
                
                if all(k in raw_data for k in ['gold_18k', 'gold_24k', 'usd']):
                    net_worth = holdings.calculate_net_worth(
                        raw_data['gold_18k'],
                        raw_data['gold_24k'],
                        raw_data['usd']
                    )
                    
                    # Create history snapshot
                    NetWorthHistory.objects.create(
                        user=request.user,
                        net_worth=Decimal(str(net_worth)),
                        gold18_amount=holdings.gold18,
                        gold24_amount=holdings.gold24,
                        usd_amount=holdings.usd
                    )
                    
                    return JsonResponse({'status': 'success', 'message': 'Snapshot saved successfully', 'net_worth': net_worth})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Unable to fetch current rates'}, status=500)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)
