from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user, logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
# get models from the core
# get the disabled account app
from disabledAccount.models import DiabledAccount
# initialize the custom user
BASE_USER_MODEL = get_user_model()


# Create your views here.


class DisableAccount(View):
    
    success_url = settings.LOGIN_URL
    template_name = "account/actions/account_confirm_disable.html"
    context = {}
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        logged = request.user
        context = {"site_name":current_site.domain,"user":logged.custom_profile,}
        self.context.update(context)
        
        SUBJECT = "Disable Account Request"
        path_to_disable_email_txt = "account/alerts/account_disable_request.txt"
        # send the email after deletion
        self.compose_email(SUBJECT, path_to_disable_email_txt, logged, self.context).send()
        return render(request, self.template_name, self.context)
    
        
        
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # fetch current user
        logged = get_user(request)
        # compose data to be sent to the email and to the use
        
        context = {"user":logged.custom_profile.full_name,
                   "time":timezone.now,
                   "site_name": get_current_site(request).domain
                   }
        self.context.update(context)
        # compose email and send
        
        subject = "Disable Account Confirmed"
        disable_email_txt_file_path = "account/alerts/account_disable_confirm.txt"
        
        self.compose_email(subject, disable_email_txt_file_path, logged, self.context).send(fail_silently=True)
        # now disable the user and associated profile 
        # together with the Facility owned
        
        queryset = [Q(type="DOCTOR")|Q(type="PHARMACIST")|Q(type="CLINICIAN")|Q(type="PATIENT")]
        # facilities = get_list_or_404(Facility, owner=logged.custom_profile)
            
            
        # if facilities:
        #     for facility in facilities:
        #         facility.is_verified = False
        if logged.type in queryset:
            
            logged.set_unusable_password()
            logged.is_active = False
            logout(request)
        elif logged.type == "ADMIN":
                raise TypeError(_("Adminitrator cannot be disabled"))
        else:
            logged.set_unusable_password()
            logged.is_active = False
            logged.save()
            logout(request)
            DiabledAccount.objects.create(
                    account_name=logged.email,
                    date_joined=logged.date_joined,
                    date_left=timezone.now(),
                    acc_type=logged.type
                )
            # TODO: WIILL BE DELETED 
            BASE_USER_MODEL.objects.get(email=logged).delete()
        return redirect(self.success_url)
    
    def compose_email(self, subject, path_to_file, logged, context):

        message = render_to_string(path_to_file, context)
        email = EmailMessage(subject, message, to=[logged.email])
        
        return email
        
account_disable_view = DisableAccount.as_view()

