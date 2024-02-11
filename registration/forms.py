from .models import User
from .models import UserProfile

from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm

from email_validator import validate_email, EmailNotValidError

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', required=True)
    middle_name = forms.CharField(label='Middle name', required=False)
    last_name = forms.CharField(label='Last name', required=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = forms.CharField(label='Phone number', validators=[phone_regex], max_length=15, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = ''
        self.fields['username'].required = True  # Make username field required
        self.fields['first_name'].required = True  # Make first_name field required
        self.fields['last_name'].required = True  # Make last_name field required
        self.fields['email'].required = True  # Make email field required
        self.fields['phone_number'].required = True  # Make phone_number field required

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except EmailNotValidError:
            raise forms.ValidationError("Please enter a valid email address.")
        return email

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']