from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
        label='Confirm Password', 
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'email': 'Email',
        }
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        
        if password and password2:
            # Check if passwords match
            if password != password2:
                raise ValidationError("Passwords do not match")
            
            # Check minimum length
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long")
            
            # Check for at least one letter
            if not any(char.isalpha() for char in password):
                raise ValidationError("Password must contain at least one letter")
            
            # Check for at least one digit
            if not any(char.isdigit() for char in password):
                raise ValidationError("Password must contain at least one number")
        
        return self.cleaned_data['password2']
