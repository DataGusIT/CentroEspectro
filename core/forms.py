# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu e-mail'}))
    first_name = forms.CharField(max_length=100, required=True, label='Nome', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}))
    last_name = forms.CharField(max_length=100, required=True, label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu sobrenome'}))
    username = forms.CharField(max_length=100, required=True, label='Nome de usuário', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}))
    password1 = forms.CharField(max_length=50, required=True, label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Sua senha'}))
    password2 = forms.CharField(max_length=50, required=True, label='Confirmar senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True, label='Nome de usuário', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}))
    password = forms.CharField(max_length=50, required=True, label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Sua senha'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True, label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=True, label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']