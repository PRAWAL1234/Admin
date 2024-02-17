from typing import Any
from django import forms
from django.contrib.auth.models import User

class form(forms.Form):
    first_name=forms.CharField(max_length=255,widget=forms.TextInput(attrs={'placeholder':'First Name','id':'first_name','name':'first_name'}))
    last_name=forms.CharField(max_length=255,widget=forms.TextInput(attrs={'placeholder':'Last Name','id':'last_name','name':'last_name'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email','id':'email','name':'email'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username','id':'username','name':'username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','id':'password','name':'password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','id':'confirm_password','name':'confirm_password'}))

    def clean(self):
        x=super().clean()

        if x['password'] != x['confirm_password']:
            raise forms.ValidationError('Password Not Match')
        if User.objects.filter(email=x['email']).exists():
            raise forms.ValidationError('Email Already Exists')
        if User.objects.filter(username=x['username']).exists():
            raise forms.ValidationError('Username Already Exists')