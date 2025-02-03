from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BackupJobViewSet

router = DefaultRouter()
router.register(r'backupjobs', BackupJobViewSet)

urlpatterns = [
    path('/', include(router.urls)),
]
