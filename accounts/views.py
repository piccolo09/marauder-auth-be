from django.contrib.auth import get_user_model
from rest_framework.decorators import action, api_view
from rest_framework import response, status
from rest_framework_simplejwt.views import TokenObtainPairView
from djoser.views import UserViewSet
from djoser.conf import settings as djoser_settings
from django.conf import settings as _settings
from djoser.compat import get_user_email
from djoser import signals
from .tokens import invite_accept_token
from .emails import InvitationEmail
from .serializers import (
    CustomTokenObtainPairSerializer, PublicUserSerializer,CustomSendEmailResetSerializer,
    UserInviteSerializer, InvitationTokenSerializer
    )
import jwt
User = get_user_model()


class TokenGenratorView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserManagementViewset(UserViewSet):
    invite_token_generator = invite_accept_token

    def get_permissions(self):
        if self.action == "invite":
            self.permission_classes = djoser_settings.PERMISSIONS.password_reset
        elif self.action == "invite_resend":
            self.permission_classes = djoser_settings.PERMISSIONS.password_reset
        elif self.action == "invite_accept":
            self.permission_classes = djoser_settings.PERMISSIONS.activation

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "invite":
            # TODO: Sync up with settings
            return UserInviteSerializer
        elif self.action == "invite_resend":
            # TODO: Sync up with settings
            return CustomSendEmailResetSerializer
        elif self.action == "invite_accept":
            return InvitationTokenSerializer
        return super().get_serializer_class()

    def reset_username(self, request, *args, **kwargs):
        """
        Supressing method
        """
        pass

    def set_username(self, request, *args, **kwargs):
        """
        Supressing method
        """
        pass

    def reset_username_confirm(self, request, *args, **kwargs):
        """
        Supressing method
        """
        pass

    @action(["post", "delete"], detail=False)
    def invite(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [get_user_email(user)]
        # TODO CONVERT TO SETTINGS:
        InvitationEmail(self.request, context).send(to)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(["post"], detail=False)
    def invite_resend(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # can only resend invite to users without a valid password and inactive account
        user = serializer.get_invited_user()
        if not user:
            return response.Response("Invitation already Accepted.", status=status.HTTP_400_BAD_REQUEST)
        context = {"user": user}
        to = [get_user_email(user)]
        # TODO Sync up with SETTINGS:
        InvitationEmail(self.request, context).send(to)
        return response.Response(status=status.HTTP_202_ACCEPTED)

    @action(["post"], detail=False)
    def invite_accept(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if hasattr(user, "activated"):
            user.activated = True
        user.save()
        data_to_setup = self.get_safe_user_repr(user)
        # resp = djoser_settings.SERIALIZERS.current_user(user)
        data_to_setup.update({
            "token": self.token_generator.make_token(user),
            "uid": serializer.initial_data.get("uid", "")
            })
        return response.Response(data=data_to_setup,status=status.HTTP_200_OK)

    @action(["post"], detail=False)
    def setup_profile(self, request, *args, **kwargs):
        pass

    def get_safe_user_repr(self,user):
            return{
                "first_name": getattr(user, "first_name", ""),
                "last_name": getattr(user, "last_name", ""),
                }


@api_view(['GET'])
def get_public_key(request):
    """
        GET PUBLIC KEY FOR JWT TOKEN VERIFICATION FOR INTEGRATION WITH OTHER APPS 
    """
    response_content, status_code = None, status.HTTP_403_FORBIDDEN
    if "HS" not in _settings.SIMPLE_JWT.get('ALGORITHM', ''):
        response_content = {
            "alg": _settings.SIMPLE_JWT.get('ALGORITHM', False),
            "use": _settings.PUBLIC_KEY
            }
        status_code = status.HTTP_200_OK
    return response.Response(response_content, status=status_code)
