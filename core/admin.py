from django.contrib import admin
from .models import Facility
from core.helper.extra import Service
# actions
from core.Admin.actions import make_verified_facility

# inlines

from core.Admin.inlines import (
    ReviewInline ,FacilityImageInline ,FacilityAwardInline, FaciliTyWorkingDayInline, 
    FacilityBranchImageInline, FacilityBranchImageInline, FacilityBranchInline
)
# Register your models here.


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("service", )



@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = [
        "owner", "name","location","is_verified", "category",
        ]
    inlines = [
        FaciliTyWorkingDayInline,
        ReviewInline, FacilityImageInline, FacilityAwardInline, FacilityBranchInline,
        
        ]
    
    actions = [make_verified_facility, ]
