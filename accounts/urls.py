# from django.urls import path
from .views import UserInvitationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("invite", UserInvitationViewSet)


urlpatterns = router.urls
