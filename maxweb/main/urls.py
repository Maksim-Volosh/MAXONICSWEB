from django.contrib import admin
from django.urls import include, path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name="home"),
    path('register/', register, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('how_to_order/', how_to_order, name='how_to_order'),
    path('create_order/', create_order, name='create_order'),
    path('order/delete/<int:order_id>/', delete_order, name='delete_order'),
    path('portfolio/', portfolio, name='portfolio'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
