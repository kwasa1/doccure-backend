from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# this is a custom authentication backend
# django userse by default
# --->django.contrib.auth.backends.ModelBackend

class PasswordLessAuthentication(ModelBackend):
    # logging without giving password
    
    def authenticate(self, request, email):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
