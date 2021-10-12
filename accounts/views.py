from django.db import transaction 
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins,status, generics, status, views
from djoser.conf import settings
from djoser.compat import get_user_email
from rest_framework.decorators import action
from .serializers import UserInviteSerialiser,AcceptInviteSeralizer
from rest_framework.response import Response
from .email import InvitationEmail
from djoser import utils
from .tokens import invite_accept_token,password_reset_token
from marauder_utils.views import ActionBasedSerializerMixin
User = get_user_model()


class UserInvitationViewSet(ActionBasedSerializerMixin,mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserInviteSerialiser
    lookup_field = settings.USER_ID_FIELD
    # permission_classes = (AllowAny,)
    serializer_class_by_action = {
        "create":UserInviteSerialiser,
        "accept_invite":AcceptInviteSeralizer,
    }
    token_generator = invite_accept_token


    @action(["post"], detail=False)
    def invite(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        context = {"user": user}
        to = [get_user_email(user)]
        InvitationEmail(self.request, context).send(to)

    @action(["post"], detail=False)
    @transaction.atomic
    def accept_invite(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        user = self.serializer_class(serializer.user).data
        user.update(
            {
                "uid": utils.encode_uid(serializer.user.pk),
                "password_setup_key": password_reset_token.make_token(serializer.user)
            }
        )
        return Response(user, status=status.HTTP_202_ACCEPTED)
