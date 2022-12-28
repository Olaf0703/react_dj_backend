from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None:
            UserModel = get_user_model()

            try:
                user = UserModel.objects.get(email__iexact=username)
            except UserModel.DoesNotExist:
                """Not found, try another backend"""
            else:
                if user.check_password(password) and user.is_active:
                    return user
            return None
