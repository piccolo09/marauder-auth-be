from templated_mail.mail import BaseEmailMessage
from djoser import utils, email
from .tokens import invite_accept_token
from djoser.conf import settings
from djoser.compat import get_user_email

class InvitationEmail(BaseEmailMessage):

    template_name = "email/invitation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        print(user.has_usable_password(),"AA")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = invite_accept_token.make_token(user)
        context["url"] = settings.INVITATION_URL.format(**context)
        return context


class ConfirmationEmail(email.ActivationEmail):
    template_name = "email/confirm_email_address.html"
    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        print(context)
        context["first_name"] = "" if getattr(user,"first_name","") == None else getattr(user,"first_name","")
        return context

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "email/password_reset_v1.html"