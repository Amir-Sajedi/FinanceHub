from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserHolding(models.Model):
    """Store user's asset holdings: gold 18k, gold 24k, and USD"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='holdings', verbose_name='کاربر')
    gold18 = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name='طلای ۱۸ عیار', help_text='طلای ۱۸ عیار به گرم')
    gold24 = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name='طلای ۲۴ عیار', help_text='طلای ۲۴ عیار به گرم')
    usd = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='دلار آمریکا', help_text='دلار آمریکا')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    class Meta:
        verbose_name = 'دارایی کاربر'
        verbose_name_plural = 'دارایی‌های کاربران'

    def __str__(self):
        return 'دارایی‌های {}'.format(self.user.username)

    def calculate_net_worth(self, gold18_price, gold24_price, usd_price):
        """
        Calculate total net worth in IRR using live rates.

        Args:
            gold18_price: Price per gram of 18K gold in IRR
            gold24_price: Price per gram of 24K gold in IRR
            usd_price: USD to IRR exchange rate

        Returns:
            Total net worth in IRR (float)
        """
        gold18_value = float(self.gold18) * float(gold18_price)
        gold24_value = float(self.gold24) * float(gold24_price)
        usd_value = float(self.usd) * float(usd_price)
        return gold18_value + gold24_value + usd_value


class NetWorthHistory(models.Model):
    """Track net worth over time for charting purposes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='networth_history', verbose_name='کاربر')
    net_worth = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='ارزش خالص دارایی', help_text='ارزش خالص دارایی به ریال')
    gold18_amount = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name='مقدار طلای ۱۸ عیار')
    gold24_amount = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name='مقدار طلای ۲۴ عیار')
    usd_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='مقدار دلار آمریکا')
    timestamp = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='زمان ثبت')

    class Meta:
        verbose_name = 'ثبت وضعیت دارایی'
        verbose_name_plural = 'ثبت‌های وضعیت دارایی'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]

    def __str__(self):
        return '{} ـ {} ریال در {}'.format(
            self.user.username,
            self.net_worth,
            self.timestamp.strftime('%Y-%m-%d %H:%M'),
        )
