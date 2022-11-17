from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from account.cipher import account_activator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
User = get_user_model()


ACCOUNT_TYPE = (
    ("DOCTOR", "Doctor"),
    ("PATIENT", "Patient"),
    ("PHARMACIST", "Pharmacist"),
    ("CLINICIAN", "Clinician")
)


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Your Email Address", widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder": "example@gmail.com"
    }))
    phone_number = forms.CharField(label="Your phone number", widget=forms.NumberInput(attrs={
        "class":"form-control",
        "placeholder":"+(code) xx xxx xxxx"
    }))
    
    type = forms.ChoiceField(label="Select Account Type", choices=ACCOUNT_TYPE, widget=forms.Select(attrs={
        "class":"form-control floating",
    }), required=True, disabled=False)
    
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user= User.objects.get(email=email)
            if user:
                raise forms.ValidationError(_("The email is already registered"))
        except:
            return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        try:
            user = User.objects.get(phone_number=phone_number)
            if user:
                raise forms.ValidationError(_("Phone number is already registered"))
        except:
            return phone_number
    
    def cleaned_type(self):
        account_type = self.cleaned_data.get("type")
        return account_type
    
    def save_new_user(self):
        user = None
        try:
            user = User.objects.create(
                email=self.clean_email(),
                phone_number=self.clean_phone_number(),
                type=self.cleaned_type(),
            )
            user.is_active=False
            user.save()
        except:
            raise ValueError(_("User those credentials already exists!"))
        
        return user
    
    
    # We need the user object, so it's an additional parameter
    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        SUBJECT = 'ACCOUNT ACTIVATION'
        if request.is_secure() or not settings.DEBUG: protocol="https"
        else: protocol =  "http"
        context = {
                "protocol":protocol,
                'user': user,
                'domain': current_site.domain,
                "site_name":current_site.name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activator.make_token(user),
            }
        message = render_to_string(
            'account/partials/activate.txt',
            context
        )
        
        send_mail(subject=f"{settings.DEFAULT_FROM_EMAIL}- {SUBJECT}", message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user.email])
        return context


class LoginForm(forms.Form):
    email = forms.EmailField(label="Enter your email address", widget=forms.EmailInput(attrs={
        "class":"form-control",
    }))
    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.get(email=email)
        if not user:
            raise forms.ValidationError(_("No account is associated this email."))
        return email