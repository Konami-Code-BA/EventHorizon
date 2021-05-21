from django.contrib import admin
from django.urls import path, include
from .routers import router
from app_name.views import example


urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/', include(router.urls)),
		path('webhook/', example)
]
