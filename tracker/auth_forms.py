from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Activity

class CustomUserCreationForm(UserCreationForm):
    """Form registrasi user dengan field tambahan"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    full_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nama Lengkap (Opsional)'
    }))

    class Meta:
        model = User
        fields = ("username", "email", "full_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Konfirmasi Password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Buat UserProfile
            UserProfile.objects.create(
                user=user,
                full_name=self.cleaned_data.get("full_name", "")
            )
        return user


class ActivityForm(forms.ModelForm):
    """Form untuk membuat/edit aktivitas"""
    class Meta:
        model = Activity
        fields = ['name', 'time']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama aktivitas...'
            }),
            'time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Waktu (contoh: 08:00 - 10:00)'
            })
        }


class ProfileUpdateForm(forms.ModelForm):
    """Form untuk update profil user"""
    class Meta:
        model = UserProfile
        fields = ['full_name', 'timezone', 'avatar']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'timezone': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('Asia/Jakarta', 'WIB - Jakarta'),
                ('Asia/Makassar', 'WITA - Makassar'),
                ('Asia/Jayapura', 'WIT - Jayapura'),
            ]),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }