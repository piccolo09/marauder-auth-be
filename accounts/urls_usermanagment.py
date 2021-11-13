
from django.contrib.auth import get_user_model
from .views import UserManagementViewset
from rest_framework.routers import DefaultRouter

from djoser import views

router = DefaultRouter()
router.register("users", UserManagementViewset)

User = get_user_model()

urlpatterns = router.urls