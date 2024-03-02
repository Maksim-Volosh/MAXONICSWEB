from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from django.contrib.auth.validators import ASCIIUsernameValidator
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        placeholders = kwargs.pop('placeholders', {
            'username': _('Username'),
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email'),
            'password1': _('Enter your password'),
            'password2': _('Enter your password again'),
        })

        super().__init__(*args, **kwargs)
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({'placeholder': placeholder})
        
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) and field_name.startswith('password'):
                field.widget.attrs.update({'pattern': '[a-zA-Z0-9]+', 'title': _('Password must contain only Latin letters and digits')})

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }




    
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Username'), }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Password'),}))
    
    
    
    
    
class OrderForm(forms.ModelForm):

    budget = forms.DecimalField(label='Бюджет (€)')
    
    socialnetwork = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget()
    )
    
    class Meta:
        model = OrderCreate
        exclude = ['status', 'user']
        fields = ['name', 'description', "targetgroup", 'websitetype', 'budget', 'socialnetworkchose' , 'socialnetwork', 'deadline', 'files']
        placeholders = {
            'name': _('Order name'),
            'description': _('Description of your project, what you want to see, what features you want to implement'),
            'targetgroup': _('Who is your target audience?'),
            'websitetype': _('Select website type'),
            'budget': _('Budget (€)'),
            'socialnetworkchose': _("Select communication type"),
            'socialnetwork': _("Phone number"),
            'deadline': _('Desired deadline'),
            'files': _('Files'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, placeholder in self.Meta.placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})
            self.fields[field_name].required = True
        self.fields['files'].required = False

