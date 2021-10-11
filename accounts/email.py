# from templated_mail import BaseEmailMessage
from templated_mail.mail import BaseEmailMessage
from djoser import utils
from .tokens import invite_accept_token
from djoser.conf import settings

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