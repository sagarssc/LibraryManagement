from django.urls import path

from .views import UserViewSet
from rest_framework import routers


urlpatterns = []

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns += router.urls