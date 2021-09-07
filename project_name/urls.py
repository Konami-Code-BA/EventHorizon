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
    path('front/', index, name='index'),
    path('loginRegister/', index, name='index'),
    path('registerWithEmail/', index, name='index'),
    path('loginWithEmail/', index, name='index'),
    path('settings/', index, name='index'),
    path('hostAdmin/', index, name='index'),
    path('hostProfile/', index, name='index'),
    path('guestHome/', index, name='index'),
    path('experiment1/', index, name='index'),
    path('experiment2/', index, name='index'),
    path('password_reset/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
