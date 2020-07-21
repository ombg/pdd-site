from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pdd import views


router = DefaultRouter()
router.register('videos', views.VideoObjViewSet)

app_name = 'pdd'

urlpatterns = [
    # Include all URLs generated by default router
    path('', include(router.urls)),
]
