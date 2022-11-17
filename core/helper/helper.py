from django.db import models
from core.models import Facility
from django.utils.translation import gettext_lazy as _
from account.models import Profile
from core.models import FacilityBranch
User = Profile




    
class Award(models.Model):
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    year = models.DateField()
    about = models.CharField(max_length=500)


class WorkingDay(models.Model):
    class OperationDays(models.TextChoices):
        M = "M", "Monday"
        T= " T", "Tuesday"
        W="W", "Wednesday"
        TH="TH", "Thursday"
        F="F", "Friday"
        S="S", "Saturday"
        SU ="SU", "Sunday"
        
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="working_day")
    branch = models.ForeignKey(FacilityBranch, on_delete=models.CASCADE, related_name="branch_working_day")
    day = models.CharField(_("Operational Days; Monday"), max_length=2,blank=True, null=True,
                           choices=OperationDays.choices, default=OperationDays.M)
    openning_time = models.TimeField(auto_now=False)
    closing_time = models.TimeField(auto_now=False)
    
    
    def __str__(self):
        return self.day
 

class Review(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="facility_review")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_author")
    title = models.CharField(max_length=70)
    review = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.title} review"
 