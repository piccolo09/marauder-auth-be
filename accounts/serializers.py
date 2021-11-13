from django.contrib.auth import get_user_model
from djoser.serializers import SendEmailResetSerializer, UidAndTokenSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from djoser.conf import settings as djoser_settings
from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from djoser import utils

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "pk","groups")

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "pk")

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['last_login'] = str(user.last_login)
        token['email'] = user.email
        return token

class UserTweaksMixin:
    def get_invited_user(self):
        try:
            user = User._default_manager.get(
                is_active=False,
                **{self.email_field: self.data.get(self.email_field, "")},
            )
            if not user.has_usable_password():
                return user
        except User.DoesNotExist:
            pass
        self.fail("email_not_found")



class CustomSendEmailResetSerializer(UserTweaksMixin, SendEmailResetSerializer):
    pass


class UserInviteSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    # default_error_messages = {
    #     "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    # }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            djoser_settings.LOGIN_FIELD,
            djoser_settings.USER_ID_FIELD,
            "first_name", "last_name"
            # "password",
        )

    def validate(self, attrs):
        user = User(**attrs)
        # password = attrs.get("password")

        # try:
        #     validate_password(password, user)
        # except django_exceptions.ValidationError as e:
        #     serializer_error = serializers.as_serializer_error(e)
        #     raise serializers.ValidationError(
        #         {"password": serializer_error["non_field_errors"]}
        #     )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            # TODO: Sync up with settings
            # if settings.SEND_ACTIVATION_EMAIL:
            user.is_active = False
            if hasattr(user, "activated"):
                user.activated = False
            user.set_unusable_password()
            user.save()
        return user

class InvitationTokenSerializer(UidAndTokenSerializer):

    default_error_messages = UidAndTokenSerializer.default_error_messages
    default_error_messages.update({"password_set":"Profile is Setup, Login to Continue"})

    def validate(self, attrs):

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

        if (self.user.activated and not self.user.has_usable_password()):
            return attrs

        if (self.user.has_usable_password() and not self.user.activated) or (self.user.has_usable_password() and self.user.is_active):
            key_error = "password_set"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )

        is_token_valid = self.context["view"].\
            invite_token_generator.check_token(
            self.user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return attrs
        else:
            key_error = "invalid_token"
            raise ValidationError(
                {"token": [self.error_messages[key_error]]}, code=key_error
            )

