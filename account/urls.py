from django.urls import path, include
from . import views
from authentication.views import register_page

app_name = "account"
urlpatterns = [
    
    path("disable/", views.account_disable_view, name="disable_account"),
    ]
