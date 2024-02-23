from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from django.contrib.auth.validators import ASCIIUsernameValidator
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        placeholders = kwargs.pop('placeholders', {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'password1': 'Введите ваш пароль',
            'password2': 'Введите ваш пароль еще раз',
        })
        super().__init__(*args, **kwargs)
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({'placeholder': placeholder})
        
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) and field_name.startswith('password'):
                field.widget.attrs.update({'pattern': '[a-zA-Z0-9]+', 'title': 'Пароль должен содержать только латинские буквы и цифры'})

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
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль',}))
    
    
    
    
    
class OrderForm(forms.ModelForm):

    budget = forms.DecimalField(label='Бюджет (€)')
    
    class Meta:
        model = OrderCreate
        exclude = ['status', 'user']
        fields = ['name', 'description', "targetgroup", 'websitetype','budget', 'deadline', 'files']
        placeholders = {
            'name': 'Название заказа',
            'description': 'Описание вашего проекта, что хотите видеть, какие функции хотите реализовать',
            'targetgroup': 'Какая ваша целевая аудитория?',
            'websitetype': 'Выберите тип сайта',
            'budget': 'Бюджет (€)',
            'deadline': 'Желаемый срок',
            'files': 'Файлы',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, placeholder in self.Meta.placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})
            self.fields[field_name].required = True
        self.fields['files'].required = False

