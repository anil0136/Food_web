from django import forms
from accounts.models import UserRegister
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        # fields="__all__"
        fields =['username','email','password']

class UserDetails(forms.ModelForm):
    class Meta:
        model=UserRegister
        # fields="__all__"
        fields =['phone','house_no','street','city','state','zipcode','userpic']
    captcha = ReCaptchaField()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields =['username','email']
        
class UserRegisterUpdateForm(forms.ModelForm):
    class Meta:
        model=UserRegister
        fields=['phone','house_no','street','city','state','zipcode','userpic']


class ForgotPasswordForm(forms.Form):
    identifier = forms.CharField(
        label="Username or Email",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control-custom", "placeholder": "Enter username or email"})
    )


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control-custom", "placeholder": "New password"})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control-custom", "placeholder": "Confirm password"})
    )
