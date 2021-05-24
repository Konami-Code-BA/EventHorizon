from django.contrib import admin
from django.urls import path, include
from .routers import router
from app_name.views import example
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/', include(router.urls)),
		path('webhook/', example),
    path("", TemplateView.as_view(template_name="application.html"), name="app"),
]
