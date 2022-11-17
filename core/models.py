from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from account.models import Profile
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from core.helper.extra import Service

User = Profile


Category = (("PHARM", "Pharmacy"), ("CLINIC", "Clinic"), ("LAB", "Laboratory"))


def upload_path(user):
    return f"users/facility/"

class FacilityImage(models.Model):
    name = models.ForeignKey("Facility", on_delete=models.CASCADE, related_name="facility_pic")
    pic = models.ImageField(upload_to=upload_path(User))
    
    def __str__(self):
        return f"{self.name.name}' Image"


class Facility(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="facility_owner")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    core_services = models.TextField(blank=True, null=True)
    category = models.CharField(choices=Category, default="PHARM", max_length=20)
    services = models.ManyToManyField(Service, related_name="facility_services")
    is_verified = models.BooleanField(default=False)
    pro_pic = models.ImageField(upload_to="upload/facilities/", null=True, blank=True)
    address = models.CharField(_("96 Red Hawk Road Cyrus, MN 56323"),max_length=255, null=True, blank=True)
    about = models.CharField(max_length=1000)
    average_fee = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    phone = models.IntegerField(_("Clinics Phone Number"), blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")
        get_latest_by = "registration_date"
        ordering = ['name', "location"]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("core:facility_detail", kwargs={
            "category":self.category,
            "location":self.location,
            "name":self.name
        })
        
        
       
class FacilityBranch(models.Model):
    
    class Branch(models.TextChoices):
        TZ = "TANZANIA", "Tanzania"
        UG = "UGANDA", "Uganda"
        KE = "KENYA", "Kenya"
        SA = "SOUTH AFRICA", "South Africa"
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="facility_branch")
    branch = models.CharField(_("Facility Branches"), max_length=30, default=Branch.KE, choices=Branch.choices)
    address = models.CharField(_("96 Red Hawk Road Cyrus"), max_length=100)
    branch_pic = models.ImageField(upload_to="upload/branches/main/", null=True, blank=True)
    area = models.CharField(_("Area of specialization,i.e Neurology"), max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.branch}"

class BranchImage(models.Model):
    branch = models.ForeignKey("FacilityBranch", on_delete=models.CASCADE, related_name="branch_image")
    pic = models.ImageField(upload_to="uploads/location/branch/", blank=True, null=True)
   
    
        
        
        