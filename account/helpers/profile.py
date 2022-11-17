from django.db import models
from account.models import Profile
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ProfileReview(models.Model):
    reviewer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="account_reviewer")
    reviewed = models.ForeignKey(Profile, related_name="account_reviewed", on_delete=models.CASCADE)
    title = models.CharField(_("Review Title"), max_length=300)
    review = models.CharField(_("Review"), max_length=700)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['-pub_date']
        get_latest_by = ['pub_date']
    
    def __str__(self):
        return f"{self.title}"
    
class Specialization(models.Model):
    special = models.CharField(_("Example Orthodentist"), max_length=100, null=True, blank=True, unique=True)
    def __str__(self):
        return f"{self.special}"

class Education(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="education")
    school = models.CharField(_("Place of study"), max_length=100, blank=True, null=True)
    start_year = models.DateField(_("Start Date"), default=timezone.now)
    end_year = models.DateField(_("End Date"), default=timezone.now)
    course = models.CharField(_("Course Studied"), max_length=200, blank=True, null=True)
    website = models.URLField(_("Website Link"), max_length=255, blank=True, null=True)
    
    def __repr__(self):
        return f"{self.school!r}: {self.start_year.year!r}-{self.end_year.year!r}"
    
    @property
    def duration(self):
        return f"{self.end_year.year - self.start_year.year}"
    
    
class WorkExpirience(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="workexpirience")
    place = models.CharField(_("Place of Work"), max_length=100, blank=True, null=True)
    start_year = models.DateField(_("Start Date"), blank=True, default=timezone.now)
    end_year = models.DateField(_("End Date"), blank=True, default=timezone.now)
    website = models.URLField(_("Website Link"), max_length=255, blank=True, null=True)
    
    def __repr__(self):
        return f"{self.place!r}"
    
    @property
    def duration(self):
        return self.end_year.year - self.start_year.year
    
    
class Award(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="award")
    title = models.CharField(_("Name of tyhe award"), max_length=100, blank=True, null=True)
    year = models.DateField(_("Date Awarded"), blank=True)
    desc = models.CharField(max_length=1000)
    
    def __repr__(self):
        return f"{self.title!r}"
    
    
class Services(models.Model):
    service = models.CharField(_("i.e Tooth cleaning"), max_length=80, null=True, blank=True)
    
    def __str__(self):
        return self.service
