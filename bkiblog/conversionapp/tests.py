from decimal import Decimal, InvalidOperation
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .views import _parse_decimal


class ConverterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='converter-user',
            password='Passw0rd!',
        )

    def test_parse_decimal_zero_and_invalid(self):
        self.assertEqual(_parse_decimal('۰'), Decimal('0'))
        self.assertEqual(_parse_decimal(''), Decimal('0'))

        with self.assertRaises(InvalidOperation):
            _parse_decimal('not-a-number')

    def test_converter_uses_mocked_rates_and_has_same_currency_logic(self):
        rates = {
            'usd': 1000000,
            'iqd': 763.36,
            'usd_iqd': 1310,
            'gold_18k': {'price': 50000000},
            'gold_24k': {'price': 65000000},
            'silver_gram': {'price': 800000},
        }
        self.client.force_login(self.user)

        with patch(
            'conversionapp.views.get_market_rates',
            return_value=(rates, True),
        ):
            response = self.client.get(reverse('converter'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['exchange_rates']['usd'], rates['usd'])
        self.assertContains(response, 'fromCurrency === toCurrency')
        self.assertContains(response, 'amount < 0')
