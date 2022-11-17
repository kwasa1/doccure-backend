from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "type")


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', "type")
        
        


class AuthenticationForm(BaseAuthenticationForm):
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder":"example@gmail.com"
    }))
    password = forms.CharField(label="Password Input", widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"*******************"
    }))
    class Meta:
        fields = ["email", "password"]
        