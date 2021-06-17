from django.contrib import admin
from django.urls import path, include
from .routers import router
from app_name.views import example
from django.conf import settings
from django.conf.urls.static import static
from app_name.views import index


urlpatterns = [
		path('webhook/', example),
    path('', index, name='index'),
    path('registration', index, name='index'),
#]
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
	urlpatterns += [
    path('admin/', admin.site.urls),
    path(f'api/', include(router.urls))
	]
