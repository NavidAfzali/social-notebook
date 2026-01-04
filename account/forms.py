from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegistrationForm(forms.Form):
    gen = (
        ('m', 'male'),
        ('f', 'female'),
        ('o', 'other')
    )
    username = forms.CharField(min_length=5, widget=forms.TextInput(
        attrs={'placeholder': 'contain letters $ num.', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'example@email.com'}))
    password1 = forms.CharField(min_length=8, label='password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'At least 8 characters.'}))
    password2 = forms.CharField(min_length=8, label='confirm password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter your password'}))
    gender = forms.ChoiceField(choices=gen)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('Username already used by another person.')
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('passwords dont match.')


class UserLoginForm(forms.Form):
    username = forms.CharField(min_length=5, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter username or email.'}))
    password1 = forms.CharField(label='password', min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class EditUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('age', 'gender',)
