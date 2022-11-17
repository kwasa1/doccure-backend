from twilio.rest import Client
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic import View
# from .forms import OtpForm
from django.http import HttpResponse
from django.http import JsonResponse
from twilio.base.exceptions import TwilioRestException
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure



class SendOTP:
    def send_code(receiver):
        # get twilio client
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        # verify the client in readiness for connection
        try:
            verification = client.verify \
                        .services(settings.SERVICE_SID) \
                        .verifications \
                        .create(channel_configuration={
                            'template_id': settings.TEMPLATE_ID,
                            'from': settings.DEFAULT_FROM_EMAIL,
                            'from_name': settings.DEFAULT_FROM_NAME,
                        }, to=receiver, channel='email')

            return verification.status
        except BaseException as e:

            return HttpResponse(e)
            




class CheckOTP:
    
    def check_otp(email, secret):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        try:
            verification_check = client.verify \
                            .services(settings.SERVICE_ID)\
                            .verification_checks \
                            .create(to=email, code=secret)

            return verification_check.status
        except TwilioRestException as e:
            print(e)
            return HttpResponse(e)
            
    


def generate_otp(request):
    return render(request, 'account/actions/otp.html')


class InputOtpForValidation(View):
    template_name = "account/actions/otp.html"
    success_url = "core:home_view"
    
    def get(self, request,*args, **kwargs):
        # context={"form":self.form_class()}
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        email = request.user.email
        otp = request.POST.get("otp")
        
        status = CheckOTP.check_otp(email, otp)
        
        print(status)
        if status == "approved":
           user = authenticate(request, email=email)
           if user is not None:
               login(request, user, backend="authentication.auth_backend.PasswordlessAuthBackend")
               return redirect("core:home_view")
           else:
               messages.error(request, "WRONG OTP!")
               
        print("otp via form: {}".format(otp))
        return render(request, "account/actions/otp.html")
               
    
            
            
        