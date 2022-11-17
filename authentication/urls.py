from django.urls import path
from . import views
from .func import generate_otp

app_name = "auth"
urlpatterns = [
    path("login/", views.auth_login_view, name="auth_login"),
    path("logout", views.auth_logout_view, name="auth_logout"),
    path("user-onbording/", views.register_page, name="onboarding"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    
    # start otp verification
    # path('check/', check_otp, name="check_otp"),
    path('otp/', generate_otp, name="generate_otp"),
]



    # path('check/', check_otp, name="check_otp"),
    # path('login/', login_page,  name="login"),
    # path('otp/<int:pk>/<uuid>/', generate_otp),
