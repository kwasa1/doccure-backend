from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    
    
    def create_user(self, email, phone_number, password, **kwargs):
        if not email:
            raise ValueError(_("Email must be set"))
        email = self.normalize_email(email)
        if password is not None:
            user = self.model(email=email, phone_number=phone_number, password=password, **kwargs)
            # user.set_password(password)
            user.save()
        else:
            user = self.model(email=email, phone_number=phone_number, password=password, **kwargs)
            user.set_unusable_password(password)
            user.save()
        return user
    
    
    def create_superuser(self, email,phone_number, password, **kwargs):
        """
        Create and save a SuperUser with the given email and password.
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, phone_number, password, **kwargs)

