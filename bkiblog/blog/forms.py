from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'dir': 'auto', 'autocomplete': 'username'}),
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'dir': 'ltr', 'autocomplete': 'current-password'}),
    )

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'dir': 'ltr', 'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'dir': 'ltr', 'autocomplete': 'new-password'})
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

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2:
            # بررسی یکسان بودن رمزها
            if password != password2:
                raise ValidationError('رمزهای عبور با هم مطابقت ندارند.')

            # بررسی حداقل طول
            if len(password) < 8:
                raise ValidationError('رمز عبور باید حداقل ۸ نویسه باشد.')

            # بررسی وجود حداقل یک حرف
            if not any(char.isalpha() for char in password):
                raise ValidationError('رمز عبور باید حداقل یک حرف داشته باشد.')

            # بررسی وجود حداقل یک عدد
            if not any(char.isdigit() for char in password):
                raise ValidationError('رمز عبور باید حداقل یک عدد داشته باشد.')

        return self.cleaned_data['password2']
