from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import CustomUser

# =============================================================================
# FORMULÁRIOS DE USUÁRIOS
# =============================================================================

class CustomUserCreationForm(UserCreationForm):
    """Formulário de criação de usuário customizado"""
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Seu e-mail'
        })
    )
    first_name = forms.CharField(
        max_length=100, 
        required=True, 
        label='Nome', 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Seu nome'
        })
    )
    last_name = forms.CharField(
        max_length=100, 
        required=True, 
        label='Sobrenome', 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Seu sobrenome'
        })
    )
    username = forms.CharField(
        max_length=100, 
        required=True, 
        label='Nome de usuário', 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nome de usuário'
        })
    )
    password1 = forms.CharField(
        max_length=50, 
        required=True, 
        label='Senha', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Sua senha'
        })
    )
    password2 = forms.CharField(
        max_length=50, 
        required=True, 
        label='Confirmar senha', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirme sua senha'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        """Valida se o e-mail já existe no banco de dados"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso. Escolha outro e-mail.")
        return email

    def clean_username(self):
        """Valida se o nome de usuário já existe (método adicional para personalizar mensagem)"""
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso. Escolha outro nome de usuário.")
        return username

class CustomAuthenticationForm(AuthenticationForm):
    """Formulário de autenticação customizado"""
    username = forms.CharField(
        max_length=100, 
        required=True, 
        label='Nome de usuário', 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nome de usuário'
        })
    )
    password = forms.CharField(
        max_length=50, 
        required=True, 
        label='Senha', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Sua senha'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class UserProfileForm(forms.ModelForm):
    """Formulário de perfil do usuário"""
    first_name = forms.CharField(
        max_length=100, 
        required=True, 
        label='Nome', 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100, 
        required=True, 
        label='Sobrenome', 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        """Valida se o e-mail já existe (exceto para o usuário atual)"""
        email = self.cleaned_data.get('email')
        # Verifica se há outro usuário com este e-mail (exceto o usuário atual)
        if self.instance and self.instance.pk:
            if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Este e-mail já está em uso por outro usuário.")
        else:
            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError("Este e-mail já está em uso.")
        return email


