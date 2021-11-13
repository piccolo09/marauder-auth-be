from django.contrib.auth.tokens import PasswordResetTokenGenerator

class InviteTokenGenrator(PasswordResetTokenGenerator):

    key_salt = "accounts.tokens.InviteTokenGenrator"

    def _make_hash_value(self, user, timestamp):
        activated_flag, has_usable_pass = False,False
        if hasattr(user, "activated"):
            activated = user.activated
        if hasattr(user, "has_usable_password"):
            has_usable_pass = user.has_usable_password()

        return str(user.pk) + str(user.is_active) + str(has_usable_pass) + str(activated)+ str(timestamp)



class ProfileSetupTokenGenrator(PasswordResetTokenGenerator):

    key_salt = "accounts.tokens.ProfileSetupTokenGenrator"

    def _make_hash_value(self, user, timestamp):
        has_usable_pass, first_name, last_name, last_login = False, None, None,None
        if hasattr(user, "first_name"):
            first_name = user.first_name
        if hasattr(user, "last_name"):
            last_name = user.last_name

        if hasattr(user, "last_login"):
            last_login = user.last_login

        if hasattr(user, "has_usable_password"):
            has_usable_pass = user.has_usable_password()

        return str(user.pk) + str(first_name) + str(has_usable_pass) + str(last_login)+ str(timestamp)

invite_accept_token = InviteTokenGenrator()
profile_setup_token = ProfileSetupTokenGenrator()