from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from main.views import page_not_found

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include("main.urls"), name="glav"),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler404 = page_not_found