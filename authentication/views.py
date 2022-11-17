from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from account.forms.base import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, get_user_model, logout
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from .func import SendOTP
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from account.cipher import account_activator
from django.contrib import messages

User = get_user_model()



class UserCreationView(View):
    form_class = RegisterForm
    template_name = "account/register.html"
    context = {}
    
    def get(self, *args, **kwargs):
        # prevent logged in users from accessing the page
        if self.request.user.is_authenticated:
            return redirect("core:home_view")
        
        self.context.update({
            "form":self.form_class(),
        })
        
        return render(self.request, self.template_name, self.context)
    
    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            user = form.save_new_user()
            form.send_activation_email(self.request, user)
            context = form.send_activation_email(self.request, user)
            # web authentication, will be: This is testing
            return render(self.request, "account/partials/web_activate.html", context)
        return render(self.request, "account/partials/activation_failed.html")


register_page = UserCreationView.as_view()     


class ActivateAccount(View):
    def post(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user=None
        if user is not None and account_activator.check_token(user, token):
            user.is_active=True
            user.save()
            messages.success(request, "Activation successfull")
            return redirect("auth:auth_login")
        else:
            messages.error(request, "Token Expired. Request new token")
            return render(request, "account/partials/activation_failed.html")
        
    

activate = ActivateAccount.as_view()


class RequestActivation(View):
    pass

request_activation = RequestActivation.as_view()







   
def send_otp(request):
    pass

    
class AuthLoginView(View):
    form_class = LoginForm
    template_name = "account/login.html"
    success_url = ""
    context = {}
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            return redirect("core:home_view")
        self.context.update({"form":self.form_class(), "site_name":get_current_site(self.request).domain})
        return render(self.request, self.template_name, self.context)
    
    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            email = form.clean_email()
            # not need to do verification here already verified at the forms level
            # will rich her only if the form part was validatd
            user = User.objects.get(email=email)
            # now send the otp to the cleaned email and redirect to otp page
            SendOTP.send_code(email)
            temp = uuid.uuid4()
            return redirect("auth:generate_otp")
        else:
            messages.error(self.request, "Invalid Email Address")
        
            
    

auth_login_view = AuthLoginView.as_view()


def auth_logout_view(request):
    logout(request)
    return redirect("core:home_view")

