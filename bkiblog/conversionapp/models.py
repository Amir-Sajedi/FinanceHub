from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserHolding(models.Model):
    """Store user's asset holdings: gold 18k, gold 24k, and USD"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='holdings')
    gold18 = models.DecimalField(max_digits=12, decimal_places=3, default=0, help_text="Gold 18K in grams")
    gold24 = models.DecimalField(max_digits=12, decimal_places=3, default=0, help_text="Gold 24K in grams")
    usd = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="US Dollars")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Holding"
        verbose_name_plural = "User Holdings"

    def __str__(self):
        return f"{self.user.username}'s Holdings"

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='networth_history')
    net_worth = models.DecimalField(max_digits=18, decimal_places=2, help_text="Net worth in IRR")
    gold18_amount = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    gold24_amount = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    usd_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name = "Net Worth History"
        verbose_name_plural = "Net Worth Histories"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.net_worth} IRR @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
