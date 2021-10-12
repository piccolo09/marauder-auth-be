from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.conf import settings
from django.db import IntegrityError, transaction
from djoser import utils
User = get_user_model()


class UserInviteSerialiser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        fields = ("email", "first_name", "last_name")
        # , "groups"

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data, password=None)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class AcceptInviteSeralizer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        "invalid_token": settings.CONSTANTS.messages.INVALID_TOKEN_ERROR,
        "invalid_uid": settings.CONSTANTS.messages.INVALID_UID_ERROR,
        "setup_complete": "You can now continue to login"
    }

    def is_setup_complete(self) -> bool:
        """
        To check if the us has completed the invitation workflow
        i.e accept invite and setup password

        @returns:
            True: If user has a usable password, is_active & accepted_invite flags are true
            False: Does not have a usable password

        @depends:
            self.user
        """
        if not self.user:
            return False
        if self.user.has_usable_password() and self.user.is_active and self.user.activated:
            key_error = "setup_complete"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )
            return True
        else:
            return False

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            uid = utils.decode_uid(self.initial_data.get("uid", ""))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )
        self.is_setup_complete()

        is_token_valid = self.context["view"].token_generator.check_token(
            self.user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            key_error = "invalid_token"
            raise ValidationError(
                {"token": [self.error_messages[key_error]]}, code=key_error
            )

    def activate(self):
        if not self.user:
            self.fail("activation called before validation")
        self.user.activated = make_aware(datetime.now())
        self.user.is_active = True
        self.user.email_confirmed = make_aware(datetime.now())
        self.user.save()
        return self.user
