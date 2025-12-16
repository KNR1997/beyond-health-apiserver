from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        username can be email OR mobile_number
        """
        if username is None or password is None:
            return None

        try:
            user = User.objects.get(
                Q(email__iexact=username) | Q(mobile_number=username)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
