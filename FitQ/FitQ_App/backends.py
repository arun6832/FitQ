from django.contrib.auth.backends import ModelBackend
from .models import Trainer

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Trainer.objects.get(email=username.lower())
            if user.check_password(password):
                return user
        except Trainer.DoesNotExist:
            return None