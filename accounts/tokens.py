from django.contrib.auth.tokens import PasswordResetTokenGenerator


class InviteTokenGenrator(PasswordResetTokenGenerator):

    key_salt = "accounts.tokens.InviteTokenGenrator"

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(user.activated) + str(timestamp)

invite_accept_token = InviteTokenGenrator()
password_reset_token = PasswordResetTokenGenerator()
