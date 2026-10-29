from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from . import messages as auth_messages


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'dir': 'auto', 'autocomplete': 'username'}),
        error_messages={'required': auth_messages.REQUIRED},
    )
    password = forms.CharField(
        label='رمز عبور',
        strip=False,
        widget=forms.PasswordInput(attrs={'dir': 'ltr', 'autocomplete': 'current-password'}),
        error_messages={'required': auth_messages.REQUIRED},
    )
    error_messages = {
        'invalid_login': auth_messages.INVALID_CREDENTIALS,
        'inactive': auth_messages.INACTIVE_ACCOUNT,
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                inactive_user = User.objects.filter(
                    username=username, is_active=False
                ).first()
                if inactive_user and inactive_user.check_password(password):
                    raise ValidationError(
                        self.error_messages['inactive'], code='inactive'
                    )
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'dir': 'ltr', 'autocomplete': 'new-password'}),
        error_messages={'required': auth_messages.REQUIRED},
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'dir': 'ltr', 'autocomplete': 'new-password'}),
        error_messages={'required': auth_messages.REQUIRED},
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'dir': 'auto', 'autocomplete': 'username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'dir': 'auto', 'autocomplete': 'given-name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'dir': 'ltr', 'autocomplete': 'email'}),
        }
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'email': 'رایانامه',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages.update({
            'required': auth_messages.REQUIRED,
            'unique': auth_messages.DUPLICATE_USERNAME,
        })
        self.fields['email'].error_messages['invalid'] = auth_messages.INVALID_EMAIL

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(auth_messages.DUPLICATE_USERNAME)
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError(auth_messages.DUPLICATE_EMAIL)
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2:
            if password != password2:
                raise ValidationError(auth_messages.PASSWORD_MISMATCH)

            if len(password) < 8:
                raise ValidationError(auth_messages.PASSWORD_TOO_SHORT)

            if password.isdigit():
                raise ValidationError(auth_messages.PASSWORD_ENTIRELY_NUMERIC)

            if not any(char.isalpha() for char in password):
                raise ValidationError(auth_messages.PASSWORD_NO_LETTER)

            if not any(char.isdigit() for char in password):
                raise ValidationError(auth_messages.PASSWORD_NO_DIGIT)

            user = User(
                username=self.cleaned_data.get('username', ''),
                first_name=self.cleaned_data.get('first_name', ''),
                email=self.cleaned_data.get('email', ''),
            )
            try:
                validate_password(password, user=user)
            except ValidationError as error:
                translated = {
                    'password_too_short': auth_messages.PASSWORD_TOO_SHORT,
                    'password_too_common': auth_messages.PASSWORD_TOO_COMMON,
                    'password_entirely_numeric': auth_messages.PASSWORD_ENTIRELY_NUMERIC,
                    'password_too_similar': auth_messages.PASSWORD_TOO_SIMILAR,
                }
                messages = []
                for item in error.error_list:
                    code = getattr(item, 'code', None)
                    fallback = item.messages[0] if item.messages else str(item)
                    messages.append(translated.get(code, fallback))
                raise ValidationError(messages)

        return password2
