from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
import messenger.settings as settings

urlpatterns = [
    path('site/django/admin/', admin.site.urls),
    path('site/js/api/', include('api.urls', namespace='api')),
    path('', include('users.urls', namespace='users'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
