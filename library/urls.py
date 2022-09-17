from django.urls import path

from .views import BookViewSet, BorrowViewSet
from rest_framework import routers


urlpatterns = []

router = routers.DefaultRouter()
router.register('', BookViewSet, basename='book')
router.register('borrow', BorrowViewSet, basename='borrow')

urlpatterns += router.urls