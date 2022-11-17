from django.contrib import admin

# from helpers

from account.helpers.profile import Education, WorkExpirience, Award, ProfileReview


class EducationInlines(admin.StackedInline):
    model = Education
    extra = 0
    
class WorkExpirienceInlines(admin.StackedInline):
    model = WorkExpirience
    extra = 0

class AwardInlines(admin.StackedInline):
    model = Award
    extra = 0
    
class ReviewerInline(admin.StackedInline):
    model = ProfileReview
    fk_name = "reviewer"
    
class ReviewedInline(admin.StackedInline):
    model = ProfileReview
    fk_name = "reviewed"