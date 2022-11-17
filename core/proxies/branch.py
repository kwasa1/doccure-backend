from django.db import models
from core.models import FacilityBranch, Facility


class TZManager(models.Manager):
    def get_queryset(self,*args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(branch=FacilityBranch.Branch.TZ)  
    
class TZ(Facility):
    objects = TZManager()
    class Meta:
        proxy=True

class KEManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(branch=FacilityBranch.Branch.KE)

class KE(Facility):
    objects = KEManager()
    class Meta:
        proxy=True

class UGManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(branch=FacilityBranch.Branch.UG)
        
class UG(Facility):
    objects = UGManager()
    class Meta:
        proxy=True
        
class SAManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(branch=FacilityBranch.Branch.SA)
    
class SA(Facility):
    objects = SAManager()
    class Meta:
        proxy=True
