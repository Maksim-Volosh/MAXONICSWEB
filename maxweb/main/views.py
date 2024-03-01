from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.template.defaultfilters import capfirst
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
import os
import re

from .telegrambot import send_telegram_message

from .models import CustomUser, OrderCreate
from .forms import CustomUserCreationForm, LoginUserForm, OrderForm


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
                desired_url = request.session.pop('desired_url', None)
                if desired_url:
                    return redirect(desired_url)
                else:
                    return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "main/login.html"

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        # После успешной аутентификации перенаправляем пользователя на изначальный URL
        desired_url = self.request.session.pop('desired_url', None)
        if desired_url:
            return redirect(desired_url)
        else:
            return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('home')


def how_to_order(request):
    if 'how_to_order_visited' in request.session:
        return redirect('create_order')
    else:
        request.session['how_to_order_visited'] = True
        return render(request, 'main/how_to_order.html')


def create_order(request):
    if 'how_to_order_visited' not in request.session:
        return redirect('how_to_order')
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            if 'files' in request.FILES:
                upload_files(request, request.FILES.getlist('files'))
            bot_token = "6632887294:AAEtPQZTCrztqczVyejn3NH-nLLx5aKx0zE"
            chat_id = "395671037"
            message_text = f"🚀🎉 МАКСИМ УРА! У ВАС НОВЫЙ ЗАКАЗ! 🎉🚀\n\n🔥 Название проекта: {order.name} \n\n🌟 Тип сайта: '{order.get_websitetype_display()}' \n\n👨‍💻Пользователь: { capfirst(order.user.username) } \n\n💰 Бюджет: {order.budget} € \n\n🔍💻 Хотите узнать больше? ознакомьтесь на сайте: https://voloshmaksim.pythonanywhere.com/profile/maksim_volosh/"

            send_telegram_message(bot_token, chat_id, message_text)
            message_text2 = "🚀🎉 МАКСИМ ПОЗДРАВЛЯЮ! 🎉🚀"
            send_telegram_message(bot_token, chat_id, message_text2)
            request.session['success_message'] = True
            return redirect('profile', username=request.user.username)
    else:
        form = OrderForm()
        request.session['success_message'] = False
    return render(request, 'main/create_order.html', {'form': form})

def upload_files(request, files):
    for f in files:
        with open(os.path.join(settings.MEDIA_ROOT, 'uploads', f.name), "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)

def download_file(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        return HttpResponse("Файл не найден", status=404)




def delete_order(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(OrderCreate, pk=order_id)
        order.delete()
        return redirect('profile', username=request.user.username)
    else:
        return redirect('home')






def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.user.is_staff:
        orders = OrderCreate.objects.all()
    else:
        orders = OrderCreate.objects.filter(user=user)

    if request.user.is_staff and request.user != user:
        orders = OrderCreate.objects.filter(user=user)
        return render(request, 'main/profile.html', {'user': user, 'orders': orders})

    if request.user != user:
        raise Http404("Страница не найдена")

    for order in orders:
        order.description = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', order.description)  # Жирный текст
        order.description = re.sub(r'__(.*?)__', r'<u>\1</u>', order.description)  # Подчеркнутый текст
        order.description = re.sub(r'&(.+?)&', r'<i>\1</i>', order.description)  # Курсив
    success_message = request.session.pop('success_message', False)
    return render(request, 'main/profile.html', {'user': user, 'orders': orders, 'success_message': success_message})


def portfolio(request):
    return render(request, 'main/portfolio.html')
