from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    full_name = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
        required= True
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        required= True
    )
    address1 = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
        required= True
    )
    address2 = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
        required= False
    )
    city = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        required= True
    )
    zipcode = forms.CharField(
        label="",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
        
    )
    country = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        required= True
    )
    telephone = forms.CharField(
        label="",
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone'}), 
        required= True
    )

    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'address1', 'address2', 'city', 'zipcode', 'country', 'telephone']

        exclude = ['user',]
