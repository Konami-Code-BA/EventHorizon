from django.contrib import admin
from django.urls import path, include
from .routers import router
from app_name.views import line_webhook
from django.conf import settings
from django.conf.urls.static import static
from app_name.views import index
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
	path('webhook/', line_webhook),
    path('', index, name='index'),
    path('/', index, name='index'),
    path('front/', index, name='index'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
