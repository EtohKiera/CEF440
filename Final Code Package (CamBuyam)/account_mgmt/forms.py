
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

#Defining a custom form that inherits from UserCreationForm and includes any additional fields to be included:
# class SellerCreationForm(UserCreationForm):
#     email = forms.EmailField(label='Email', required=True)
#     fname = forms.CharField(label='First name', max_length=50, required=True)
#     lname = forms.CharField(label='Last name', max_length=50, required=True)
#     town = forms.CharField(max_length=50, required=True)
   
#     class Meta:
#         model = Seller
#         fields = ('email', 'fname','lname','town','phone','password1', 'password2')
#         # widgets = {
#         #     'fname': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
#         #     'phone': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'lname': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'password1': forms.EmailInput(attrs={'class': 'form-control'}),
#         #     'password2': forms.TextInput(attrs={'class': 'form-control'}),
#         # }



#Defining a custom form that inherits from forms.ModelForm and includes any additional fields I want to include:
# This form is used for editing an existing user's information

# class SellerUpdateForm(forms.ModelForm):
#     email = forms.EmailField(label='Email', required=True)
#     name = forms.CharField(max_length=100, required=True)
#     date_of_birth = forms.DateField(required=False)
#     profile_photo = forms.ImageField(required=False)

#     class Meta:
#         model = Seller
#         fields = ('profile_photo', 'fname','lname','town','phone')


#Creating custom form that inherits from AuthenticationForm and includes an email field:
#By default, Django's authentication system uses the username field to authenticate users.
#By adding a custom username field with the label "Email", we can use the email address as the username.


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email', max_length=254)



class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

    def clean_username(self):
        return self.cleaned_data['username'].lower()

    class Meta:
        fields = ['username', 'password']