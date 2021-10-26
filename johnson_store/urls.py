from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from johnson_store.views import index, contacts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('contacts/', contacts, name="contacts"),
    path('films/', include('filmsapp.urls', namespace='films')),
    path('auth/', include('authapp.urls', namespace='auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
