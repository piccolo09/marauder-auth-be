from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView
from .views import TokenGenratorView,get_public_key

urlpatterns = [
    path("jwt/create/", TokenGenratorView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    path("jwt/publickey/", get_public_key, name="jwt-public-key"),
    path("jwt/sso/", get_public_key, name="jwt-public-key")

]