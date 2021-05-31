from rest_framework import routers
from app_name.viewsets import UserViewSet, LineViewset

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'line', LineViewset)
