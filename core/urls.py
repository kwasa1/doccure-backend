from django.urls import path
from . import views

# app name for namespace
app_name="core"
urlpatterns = [
    path("", views.home_list_view, name="home_view"),
    path("search/", views.facility_search_result, name="search_result"),
    path("facilities/", views.facility_list_view, name="facilities_list"),
    path("available-doctors/", views.doctors_list_view, name="doctors"),
    path("available-pharmacists/", views.pharmacy_list_view, name="pharmacy"),
    path("available-specialits/<str:uid>/profile/",views.doctor_profile_view, name="user_profile"),
    path("available-clinics/",views.clinic_list_view, name="clinics"),
    path("<str:location>/<str:category>/<str:name>/", views.facility_detail_view, name="facility_detail"),
    
]
