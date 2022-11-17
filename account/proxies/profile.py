from django.db import models
from account.models import Profile

# PROXY CLASS FOR PROFILE

class MaleManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(gender=Profile.Gender.MALE)
    
class Male(Profile):
    objects = MaleManager()
    class Meta:
        proxy=True
        

class FemaleManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(gender=Profile.Gender.FEMALE)
    
    
class Female(Profile):
    objects = FemaleManager()
    class Meta:
        proxy=True
        

class CustomManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(gender=Profile.Gender.CUSTOM)
