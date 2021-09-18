from rest_framework import routers
from app_name.viewsets import UserViewset, LineViewset, SecretsViewset, EventsViewset

router = routers.DefaultRouter()

router.register(r'user', UserViewset, basename='User')
router.register(r'line', LineViewset, basename='Line')
router.register(r'secrets', SecretsViewset, basename='Secrets')
router.register(r'events', EventsViewset, basename='Events')
