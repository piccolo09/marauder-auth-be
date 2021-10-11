# from django.db import models
from rest_framework import serializers
# from djoser.compat import get_user_email, get_user_email_field_name
from django.contrib.auth import get_user_model
from djoser.conf import settings
from django.db import IntegrityError, transaction

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


class UidAndTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        "invalid_token": settings.CONSTANTS.messages.INVALID_TOKEN_ERROR,
        "invalid_uid": settings.CONSTANTS.messages.INVALID_UID_ERROR,
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # uid validation have to be here, because validate_<field_name>
        # doesn't work with modelserializer
        try:
            uid = utils.decode_uid(self.initial_data.get("uid", ""))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )

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