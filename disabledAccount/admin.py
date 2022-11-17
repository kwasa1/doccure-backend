from django.contrib import admin
from .models import DiabledAccount
from django.contrib.auth import get_user_model, get_user

User = get_user_model()


def reactivate(self, request, queryset):

    user = get_user(request)
    if user.has_perms():
        return False
    print(user)
            

            
reactivate.shortdescription = "Reactivate Account"
    

@admin.register(DiabledAccount)
class DiabledAccountAminView(admin.ModelAdmin):
    list_display = ["account_name", "date_joined", "date_left", "acc_type"]
    
    actions = [reactivate, ]
