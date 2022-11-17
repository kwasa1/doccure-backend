from django import forms
from django.utils.translation import gettext_lazy as _

# class OtpForm(forms.Form):
#     otp = forms.CharField(label="Enter OTP sent to your email", widget=forms.NumberInput(attrs={
#         "class":"form-control",
#         "placeholder":"000000"
#     }))
    
#     def cleaned_otp(self):
#         otp = self.cleaned_data.get("otp")
#         if 5 < len(otp) > 6:
#             raise ValueError(_("The Otp sent is 6 digits in length"))
#         return otp