from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_order_notification(order):
    subject = 'IT - Просто У ВАС НОВЫЙ ЗАКАЗ!!'
    message = f'У ВАС НОВЫЙ ЗАКАЗ!! \n\nНазвание: "{order.name}" \n\nЦелевая аудитория: {order.targetgroup} \n\nБюджет: {order.budget}€ \n\nСрок: {order.get_deadline_display()}\n\n\n Для подробного просмотра информации заказа - "https://voloshmaksim.pythonanywhere.com" \n\n ПОЗДРАВЛЯЕМ С НОВЫМ ЗАКАЗОМ!!!! '
    recipient_list = ['maksgoza9@gmail.com']  # Здесь укажите адреса получателей
    send_mail(subject, message, from_email=None, recipient_list=recipient_list)
