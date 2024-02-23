from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from .sendemail import *
from .models import CustomUser, OrderCreate
from .forms import CustomUserCreationForm, LoginUserForm, OrderForm
from django.contrib.auth.views import LoginView
import re

def index(request):
    return render(request, 'main/index.html')




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "main/login.html"
    
    def get_success_url(self):
        return reverse_lazy('home')


def logout_view(request):
    logout(request)
    return redirect('home')


def upload_files(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
            
@login_required
def how_to_order(request):
    return render(request, 'main/how_to_order.html')
    

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            send_order_notification(order)
            if 'files' in request.FILES:
                upload_files(request.FILES.getlist('files'))
            return redirect('profile', username=request.user.username)
    else:
        form = OrderForm()
    return render(request, 'main/create_order.html', {'form': form})



@login_required
def delete_order(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(OrderCreate, pk=order_id)
        order.delete()
        return redirect('profile', username=request.user.username)
    else: 
        return redirect('home')






@login_required
def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.user.is_staff:
        orders = OrderCreate.objects.all()
    else:
        orders = OrderCreate.objects.filter(user=user)

    if request.user != user:
        raise Http404("Страница не найдена")

    for order in orders:
        order.description = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', order.description)  # Жирный текст
        order.description = re.sub(r'__(.*?)__', r'<u>\1</u>', order.description)  # Подчеркнутый текст
        order.description = re.sub(r'&(.+?)&', r'<i>\1</i>', order.description)  # Курсив

    return render(request, 'main/profile.html', {'user': user, 'orders': orders})


def portfolio(request):
    return render(request, 'main/portfolio.html')
