from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  # Update here

def generate_token(user):
    return default_token_generator.make_token(user)

def get_user_from_token(uidb64, token, User):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Update here
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            return user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None
