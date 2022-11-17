from django.contrib import admin
from core.helper.helper import Review, Award, WorkingDay
from core.models import FacilityImage, FacilityBranch, BranchImage

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    
class FacilityImageInline(admin.StackedInline):
    model = FacilityImage
    extra = 0
    
class FacilityAwardInline(admin.StackedInline):
    model = Award
    extra = 0
    
class FaciliTyWorkingDayInline(admin.StackedInline):
    model = WorkingDay
    extra = 0
    
@admin.register(BranchImage)
class FacilityBranchImageInline(admin.ModelAdmin):
    pass

class FacilityBranchInline(admin.StackedInline):
    model = FacilityBranch
    extra = 0
    inlines = [FacilityBranchImageInline, ]