import json
import logging

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import get_market_rates
from .scraper import scrape_market_prices, PriceScraperError

logger = logging.getLogger(__name__)

_FA_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
_AR_DIGITS = '٠١٢٣٤٥٦٧٨٩'


def _parse_decimal(raw):
    """Parse a decimal that may contain Persian/Arabic digits and separators."""
    from decimal import Decimal
    s = str(raw if raw is not None else '').strip()
    for i, ch in enumerate(_FA_DIGITS):
        s = s.replace(ch, str(i))
    for i, ch in enumerate(_AR_DIGITS):
        s = s.replace(ch, str(i))
    s = s.replace('٬', '').replace('،', '').replace('٫', '.')
    if s == '':
        return Decimal(0)
    return Decimal(s)

# Create your views here.


class ConversionViewView(LoginRequiredMixin, TemplateView):

    template_name = 'conversionapp/converter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'مبدل ارز و دارایی'

        try:
            # دریافت نرخ‌های لحظه‌ای بازار (با حافظه موقت؛ صفحه هرگز معطل نمی‌ماند)
            exchange_rates, _is_live = get_market_rates()
            if not exchange_rates:
                raise PriceScraperError('empty rates')

            context['exchange_rates'] = exchange_rates

        except (PriceScraperError, Exception) as e:
            logger.warning('Converter rates unavailable: %s', e)
            context['exchange_rates'] = {}
            context['error_message'] = 'نرخ‌های لحظه‌ای بازار در دسترس نیست؛ لطفاً چند دقیقه دیگر دوباره تلاش کنید.'

        return context


class NetWorthView(LoginRequiredMixin, TemplateView):
    template_name = 'conversionapp/networth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'پیگیری ارزش خالص دارایی'

        from .models import UserHolding, NetWorthHistory
        from django.db.models import Sum

        try:
            # دریافت نرخ‌های لحظه‌ای بازار (با حافظه موقت؛ صفحه هرگز معطل نمی‌ماند)
            exchange_rates, _is_live = get_market_rates()
            if not exchange_rates:
                raise PriceScraperError('empty rates')

            raw_data = {
                'gold_18k': exchange_rates['gold_18k']['price'],
                'gold_24k': exchange_rates['gold_24k']['price'],
                'usd': exchange_rates['usd'],
            }

            context['exchange_rates'] = exchange_rates

            # دریافت یا ساخت موجودی کاربر
            holdings, created = UserHolding.objects.get_or_create(user=self.request.user)
            context['holdings'] = holdings

            # محاسبه ارزش خالص امروز با نرخ‌های زنده
            if all(k in raw_data for k in ['gold_18k', 'gold_24k', 'usd']):
                net_worth = holdings.calculate_net_worth(
                    raw_data['gold_18k'],
                    raw_data['gold_24k'],
                    raw_data['usd']
                )
                context['net_worth'] = net_worth

                # محاسبه تفکیک دارایی‌ها
                context['gold18_value'] = float(holdings.gold18) * raw_data['gold_18k']
                context['gold24_value'] = float(holdings.gold24) * raw_data['gold_24k']
                context['usd_value'] = float(holdings.usd) * raw_data['usd']
            else:
                context['net_worth'] = 0
                context['gold18_value'] = 0
                context['gold24_value'] = 0
                context['usd_value'] = 0

            # تاریخچه ارزش دارایی (۳۰ روز گذشته)
            from django.utils import timezone
            from datetime import timedelta

            thirty_days_ago = timezone.now() - timedelta(days=30)
            history = NetWorthHistory.objects.filter(
                user=self.request.user,
                timestamp__gte=thirty_days_ago
            ).order_by('timestamp')

            # آماده‌سازی داده نمودار (جی‌سان تا در جاوااسکریپت معتبر باشد)
            chart_data = {
                'labels': [h.timestamp.strftime('%Y-%m-%d') for h in history],
                'values': [float(h.net_worth) for h in history]
            }
            context['chart_data'] = json.dumps(chart_data)
            context['history_count'] = history.count()

        except (PriceScraperError, Exception) as e:
            logger.warning('Net worth rates unavailable: %s', e)
            context['exchange_rates'] = {}
            context['error_message'] = 'نرخ‌های لحظه‌ای بازار در دسترس نیست؛ لطفاً چند دقیقه دیگر دوباره تلاش کنید.'
            context['net_worth'] = 0
            context['chart_data'] = '{"labels": [], "values": []}'

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

                # به‌روزرسانی موجودی‌ها (ارقام فارسی/عربی پذیرفته می‌شود)
                holdings.gold18 = _parse_decimal(request.POST.get('gold18', 0))
                holdings.gold24 = _parse_decimal(request.POST.get('gold24', 0))
                holdings.usd = _parse_decimal(request.POST.get('usd', 0))
                holdings.save()

                return JsonResponse({'status': 'success', 'message': 'دارایی‌ها با موفقیت به‌روزرسانی شد.'})
            except (InvalidOperation, ValueError) as e:
                logger.warning('Invalid holdings input: %s', e)
                return JsonResponse({'status': 'error', 'message': 'ورودی نامعتبر است.'}, status=400)

        elif action == 'save_snapshot':
            try:
                # دریافت نرخ‌های زنده
                exchange_rates, _is_live = get_market_rates()
                if not exchange_rates:
                    raise PriceScraperError('empty rates')
                raw_data = {
                    'gold_18k': exchange_rates['gold_18k']['price'],
                    'gold_24k': exchange_rates['gold_24k']['price'],
                    'usd': exchange_rates['usd'],
                }
                holdings, created = UserHolding.objects.get_or_create(user=request.user)

                if all(k in raw_data for k in ['gold_18k', 'gold_24k', 'usd']):
                    net_worth = holdings.calculate_net_worth(
                        raw_data['gold_18k'],
                        raw_data['gold_24k'],
                        raw_data['usd']
                    )

                    # ثبت تصویر وضعیت
                    NetWorthHistory.objects.create(
                        user=request.user,
                        net_worth=Decimal(str(net_worth)),
                        gold18_amount=holdings.gold18,
                        gold24_amount=holdings.gold24,
                        usd_amount=holdings.usd
                    )

                    return JsonResponse({'status': 'success', 'message': 'وضعیت با موفقیت ثبت شد.', 'net_worth': net_worth})
                else:
                    return JsonResponse({'status': 'error', 'message': 'دریافت نرخ‌های لحظه‌ای ممکن نیست.'}, status=500)
            except Exception as e:
                logger.warning('Snapshot failed: %s', e)
                return JsonResponse({'status': 'error', 'message': 'ثبت وضعیت ممکن نشد؛ لطفاً دوباره تلاش کنید.'}, status=500)

        return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر است.'}, status=400)
