from django.db import models
from account.models import CustomUser
from django.contrib.auth.models import Group

class DoctorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.DOCTOR)
    
class Doctor(CustomUser):
    objects = DoctorManager()
    
    class Meta:
        proxy = True
        
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Types.DOCTOR
            Group.objects.filter()
        return super().save(*args, **kwargs)


class PatientManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.PATIENT)
        
class Patient(CustomUser):
    class Meta:
        proxy = True
        
    objects = PatientManager()
    def save(self, *args, **kwargs):
        if not self.pk:
                self.type = CustomUser.Types.PATIENT
        return super().save(*args, **kwargs)


class PharmacistManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.PHARMACIST)
    
class Pharmacist(CustomUser):
    class Meta:
        proxy = True
        verbose_name_plural = "Pharmacists"
        
    objects = PharmacistManager()
    
    def save(self, *args, **kwargs):
        if not self.pk:
                self.type = CustomUser.Types.PHARMACIST
        return super().save(*args, **kwargs)
    
    
class ClinicianManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.CLINICIAN) 
    
class Clinician(CustomUser):
    class Meta:
        proxy = True
    def save(self, *args, **kwargs):
        if not self.pk:
                self.type = CustomUser.Types.CLINICIAN
        return super().save(*args, **kwargs)
