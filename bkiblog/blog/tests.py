from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from . import messages as auth_messages


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ali',
            email='ali@example.com',
            password='Passw0rd!',
        )

    def test_signup_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'sara',
            'first_name': 'سارا',
            'email': 'sara@example.com',
            'password': 'X7k#pQ2m',
            'password2': 'X7k#pQ2m',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='sara').exists())
        self.assertTrue(User.objects.get(username='sara').check_password('X7k#pQ2m'))

    def test_duplicate_username_rejected(self):
        response = self.client.post(reverse('register'), {
            'username': 'ali',
            'email': 'new@example.com',
            'password': 'X7k#pQ2m',
            'password2': 'X7k#pQ2m',
        })

        self.assertContains(response, auth_messages.DUPLICATE_USERNAME)
        self.assertEqual(User.objects.filter(username='ali').count(), 1)

    def test_duplicate_email_rejected(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'ali@example.com',
            'password': 'X7k#pQ2m',
            'password2': 'X7k#pQ2m',
        })

        self.assertContains(response, auth_messages.DUPLICATE_EMAIL)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_password_mismatch_shows_persian_error(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'X7k#pQ2m',
            'password2': 'X7k#pQ2n',
        })

        self.assertContains(response, auth_messages.PASSWORD_MISMATCH)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_invalid_passwords_show_persian_errors(self):
        cases = [
            ('Ab1', auth_messages.PASSWORD_TOO_SHORT),
            ('12345678', auth_messages.PASSWORD_ENTIRELY_NUMERIC),
            ('password1', auth_messages.PASSWORD_TOO_COMMON),
        ]

        for index, (password, expected_error) in enumerate(cases):
            with self.subTest(password=password):
                username = f'weak{index}'
                response = self.client.post(reverse('register'), {
                    'username': username,
                    'email': f'{username}@example.com',
                    'password': password,
                    'password2': password,
                })

                self.assertContains(response, expected_error)
                self.assertFalse(User.objects.filter(username=username).exists())

    def test_required_fields_and_invalid_email_show_persian_errors(self):
        response = self.client.post(reverse('register'), {})
        self.assertContains(response, auth_messages.REQUIRED)

        response = self.client.post(reverse('register'), {
            'username': 'badmail',
            'email': 'not-an-email',
            'password': 'X7k#pQ2m',
            'password2': 'X7k#pQ2m',
        })
        self.assertContains(response, auth_messages.INVALID_EMAIL)
        self.assertFalse(User.objects.filter(username='badmail').exists())

    def test_password_toggle_rendered_for_every_password_field(self):
        login_page = self.client.get(reverse('login'))
        self.assertContains(login_page, 'data-password-toggle', count=1)
        self.assertContains(login_page, 'aria-label="رمز عبور"')
        self.assertNotContains(login_page, 'نمایش رمز عبور')

        register_page = self.client.get(reverse('register'))
        self.assertContains(register_page, 'data-password-toggle', count=2)
        self.assertNotContains(register_page, 'پنهان کردن رمز عبور')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'ali',
            'password': 'Passw0rd!',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_wrong_credentials_show_persian_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'ali',
            'password': 'wrong-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, auth_messages.INVALID_CREDENTIALS)

    def test_inactive_account_shows_persian_error(self):
        User.objects.create_user(
            username='inactive',
            email='inactive@example.com',
            password='Passw0rd!',
            is_active=False,
        )

        response = self.client.post(reverse('login'), {
            'username': 'inactive',
            'password': 'Passw0rd!',
        })

        self.assertContains(response, auth_messages.INACTIVE_ACCOUNT)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('logout'))

        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_anonymous_user_redirected_from_protected_pages(self):
        for url_name in ('converter', 'networth'):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse('login')))

    def test_authenticated_user_can_open_converter(self):
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
