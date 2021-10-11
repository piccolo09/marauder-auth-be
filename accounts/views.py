from django.contrib.auth import get_user_model
# , update_session_auth_hash
from rest_framework import viewsets, mixins
# generics, status, views
from djoser.conf import settings
from djoser.compat import get_user_email
from rest_framework.decorators import action
from .serializers import UserInviteSerialiser
from rest_framework.permissions import AllowAny
from .email import InvitationEmail
User = get_user_model()


class UserInvitationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserInviteSerialiser
    lookup_field = settings.USER_ID_FIELD
    permission_classes = (AllowAny,)

    @action(["post"], detail=False)
    def invite(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        # self.get_object = self.get_instance
        #     return self.retrieve(request, *args, **kwargs)
        # elif request.method == "PUT":
        #     return self.update(request, *args, **kwargs)
        # elif request.method == "PATCH":
        #     return self.partial_update(request, *args, **kwargs)
        # elif request.method == "DELETE":
        #     return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        context = {"user": user}
        to = [get_user_email(user)]
        InvitationEmail(self.request, context).send(to)
        # elif settings.SEND_CONFIRMATION_EMAIL:
        #     settings.EMAIL.confirmation(self.request, context).send(to)
