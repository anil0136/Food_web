from django import forms
from vendors.models import multivendors,menubuilding,Franchise
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.models import User


class VendoruserForm(forms.ModelForm):
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)
    class Meta:
        model=User
        # fields="_all_"
        fields =['username','email','password']

class VendorRegisterForm(forms.ModelForm):
    class Meta:
        model = multivendors
        fields = ['restaurant_name','address','city','state','zip_code','restaurant_lic','restaurant_img']
    captcha = ReCaptchaField()

class MenubuildingForm(forms.ModelForm):
    class Meta:
        model= menubuilding
        fields = ['food_name','price','food_img']
class Foodupdateform(forms.ModelForm):
    class Meta:
        model = menubuilding
        fields = ['food_name','price','food_img']


class FranchiseForm(forms.ModelForm):
    class Meta:
        model = Franchise
        fields = ["total_investment","total_year_of_aggr","profit_share","description"]