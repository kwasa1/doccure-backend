from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# forms
from .__forms import CustomUserCreationForm, CustomUserChangeForm
# models
from .models import  CustomUser, Profile
# helper import 

from account.helpers.profile import Services, Specialization

# actions && routers
# from account.Admin.router import AccountModelAdmin // not used yet
from account.Admin.actions import make_subscribed, verify_health_workers

# inline 
from account.Admin.inlines import EducationInlines, WorkExpirienceInlines, AwardInlines, ReviewerInline, ReviewedInline



def send_confirmation_emails(modeladmin, request, queryset):
    for user in queryset.filter(email_confirmed=False):
        # send_confirmation_email(user)
        pass
    

send_confirmation_emails.shortdescription = "SEND CONFIRMAION EMAIL"




@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', "type",'is_staff', 'is_active',)
    list_display = ('email', "type", "profile_uid", 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', "type", 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', "type", 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', "type", "profile")
    ordering = ('email',)
    actions = (verify_health_workers, )
    
    


    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', "last_name", "is_subscribed", "profile_id", "age"]
    inlines = [
        EducationInlines, WorkExpirienceInlines, AwardInlines, ReviewerInline, ReviewedInline
        ]
    actions = [make_subscribed, ]
    
    
@admin.register(Services)
class ServicesProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass