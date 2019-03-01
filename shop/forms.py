from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Product


class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AddItem(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'thumbnail','bgc', 'description', 'size', 'active', 'merchant_id']
        # widgets = {
        #    'merchant_id': forms.HiddenInput()
        # }
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender','country','phone_number','location','birth_date']
        widgets = {
            'birth_date': forms.SelectDateWidget(years=range(1900,2100))
        }
