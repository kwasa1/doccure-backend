from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
import string
import random
from datetime import datetime
from django.urls import reverse
from account.managers.custom import CustomUserManager
from django.core.validators import RegexValidator





class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    class Types(models.TextChoices):
        DOCTOR = "DOCTOR", "Doctor"
        PATIENT = "PATIENT", "Patient"
        ADMIN = "ADMIN", "Administrator"
        PHARMACIST = "PHARMACIST", "Pharmacist"
        CLINICIAN = "CLINICIAN", "Clinician"
        
    type = models.CharField(_("Account Type"), max_length=50, choices=Types.choices, default=Types.PATIENT)
    
    email = models.EmailField(_('email address'), unique=True)
    phone_regex = RegexValidator(regex=r"^\+?1?\d{9,15}$", message="Please enter a valide phone number")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', "type"]

    objects = CustomUserManager()
    
    
    @property
    def profile_uid(self):
        return self.custom_profile.uid

    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return reverse("core:user_profile", kwargs={
            "uid":self.profile_uid
        })
   

class Profile(models.Model):
    
    def generatId(self, length):
        letters = string.ascii_uppercase
        result = "".join(random.choice(letters) for i in range(length))
        return result
    
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        CUSTOM = "C", "Custom"
        
    WORKING_HOURS = (
        ("8 AM - 12 NOON WEEKDAYS", "8 AM - 12 NOON WEEKDAYS"),
        ("12 NOON - 5 PM NOON WEEKDAYS", "12 NOON - 5 PM NOON WEEKDAYS"),
        ("8 PM - 10 PM NOON WEEKDAYS", "8 PM - 10 PM NOON WEEKDAYS"),
        ("8 AM - 12 NOON WEEKENDS", "8 AM - 12 NOON WEEKENDS")
    )
    AREA_SPECIALIZATION = (
        ("UROLOGY", "Urology"),
        ("NEUROLOGY", "Neurology"),
        ("DENTIST", "Dentist"),
        ("ORTHOPEDIC", "Orthopedic"),
        ("CARDIOLOGY", "Cardiology"),
    )
        
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="custom_profile")
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="account/", null=True, blank=True)
    title = models.CharField(_("title ie Mr. Dr. MD. etc"), max_length=50, null=True, blank=True)
    uid = models.CharField(max_length=12, unique=True, editable=False)
    phone = models.IntegerField(_("Phone Number"),  blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=1, choices=Gender.choices, default=Gender.CUSTOM)
    birth_year = models.DateField(default=datetime.now)
    speciality = models.CharField(_("MBBS, MS-General Surgery"), max_length=100, blank=True, null=True)
    address = models.CharField(_("Lithuli Avenue BS3 113, Nairobi Kenya"), max_length=200, blank=True, null=True)
    pricing = models.DecimalField(_("$10 / session (2.5 hours)"),max_digits=8, decimal_places=2, default=10.00)
    availability = models.CharField(_("Working Hours"), max_length=50, choices=WORKING_HOURS, null=True)
    area = models.CharField(_("Area of Specialization"),null=True, blank=True, max_length=100, choices=AREA_SPECIALIZATION, default="UROLOGY")
    area_icon = models.ImageField(upload_to="area/specialization/icons/", blank=True, null=True)
    services = models.ManyToManyField("Services", related_name="services")
    bio = models.CharField(_("About your self"),max_length=1000, blank=True, null=True)
    specializations = models.ManyToManyField("Specialization", related_name="specializations", blank=True)
    is_subscribed = models.BooleanField(default=False)

    
    @property
    def age(self):
        if self.birth_year == None: return 22
        else:return f"{datetime.now().year - self.birth_year.year}"
    
    def __str__(self):
        return f"{self.first_name} - {self.uid}"
    
    @property
    def unique_id(self):
        return f"{self.first_name}-{self.uid}"
    

    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def profile_id(self):
        return f"{self.uid}"
        
    def save(self, *args, **kwargs):
        self.uid =  f"{self.generatId(6)}{self.pk}" 
        super().save(*args, **kwargs)
    
    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            
    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.custom_profile.save()







