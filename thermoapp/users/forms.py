#Django
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms

User = get_user_model()

class SignUpForm(forms.Form):
    """Sign Up Form."""

    email = forms.CharField(
        label=False,
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(attrs={
            'placeholder': 'email',
            'class': 'form-control',
            'required': True
        })
    )

    password = forms.CharField(
        label=False,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'required': True
        })
    )

    password_confirmation = forms.CharField(
        label=False,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Confirme el password',
            'class': 'form-control',
            'required': True
        })
    )

    first_name = forms.CharField(
        label = False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder':'Primer nombre',
            'class': 'form-control',
            'required': True
        })
    )

    last_name = forms.CharField(
        label = False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Apellido',
            'class': 'form-control',
            'required': True
        })
    )

    username = forms.CharField(
        label=False,
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario.',
            'class': 'form-control',
            'required': False
        })
    )

    # def clean_email(self):
    #     """Email must be unique."""
    #     email = self.cleaned_data['email']
    #     email_taken = AppUser.objects.filter(email=email).exists()

    #     if email_taken:
    #         raise forms.ValidationError('El email ya está en uso.')

    #     return email 

    # def clean(self):
    #     """Verify password confirmation match."""
    #     data = super().clean()

    #     password = data['password']
    #     password_confirmation = data['password_confirmation']

    #     if password != password_confirmation:
    #         raise forms.ValidationError('Los password no coinciden.')

    #     return data 

    # def save(self):
    #     """Create user."""
    #     data = self.cleaned_data
    #     data.pop('password_confirmation')

    #     user = AppUser.objects.create_user(**data)


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):

    error_message = admin_forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])
