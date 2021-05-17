from rest_framework import routers
from app_name.viewsets import UserViewSet

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
