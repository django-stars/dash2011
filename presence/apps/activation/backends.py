from django.contrib.auth.models import User

from activation.models import ActivationKey


class UrlLoginBackend:
    def authenticate(self, key):
        try:
            _key = ActivationKey.objects.get(key=key)
        except ActivationKey.DoesNotExist:
            return None
        else:
            return _key.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
