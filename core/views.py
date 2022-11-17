from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, RedirectView
from .models import (
    Facility, FacilityImage, FacilityBranch,
    FacilityImage,FacilityBranch
                     )
from core.helper.helper import Review, Award, WorkingDay
from core.helper.extra import Service

from django.db.models.query_utils import Q
import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from account.helpers.profile import ProfileReview
from account.forms.profile import ProfileReviewForm
from core.forms.facility import FacilityReviewForm
from django.forms import model_to_dict
from account.models import Profile

User  = get_user_model()

class SpecialityListViewMixin(ListView):
    login_url = settings.LOGIN_URL
    model = None
    template_name = ""
    context_object_name = ""
    Type = ""
    count = ""
    category = ""
    
    def get_queryset(self):
        if self.Type and self.model:
            return self.model.objects.filter(type=self.Type).all()
        return super().get_queryset().all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.count] =  self.get_queryset().count()
        context[self.category] =  self.category
        context['details']="No results found"
        
        return context


    
    
    

class LandingHomeView(ListView):
    template_name = "home.html"
    model = Facility
    paginate_by = 0
    

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['doctors'] = Profile.objects.filter(user__type="DOCTOR").all()
        context['pharmacists'] = Profile.objects.filter(user__type="PHARMACIST").all()
        context['clinicians'] = Profile.objects.filter(user__type="CLINICIAN").all()
        return context



home_list_view = LandingHomeView.as_view()

    
class SearchFacilityResultView(View):
    model = Facility
    template_name = "search.html"
    page_kwargs =  "page"
    paginate_by = 0
    
    def get(self, request, *args, **kwargs):
        # get search from the url
        location = request.GET.get("location")
        category = request.GET.get("type")
        
        # fetch data records based on the search from 
        # the db
        results = Facility.objects.filter(
            Q(location__icontains=location)&Q(category__icontains=category)
        ).all()
        # ensure the fecthed data matches the 
        # client earch and then build a context dictionary to hold the data
        context = {}
        if results.exists():
            context = {
                "resultcount":results.count(),
                "location":location,
                "category":category,
                "results":results,
                "jsonResult":json.dumps(list(Facility.objects.values()))
            }
        else:
            context={'details':"No results found"}
            
        return render(self.request, self.template_name, context)
        
        
facility_search_result = SearchFacilityResultView.as_view()


class FacilityListView(ListView):
    template_name = "facility_list.html"
    queryset = Facility.objects.all()
    context_object_name = "facilities"
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['facilitycount'] = self.get_queryset().count()
        context['facilityImages'] = FacilityImage.objects.select_related("name").all()[:4]
        context['services'] = Service.objects.prefetch_related("facility_services").all()
        context['feedback'] = Review.objects.select_related("facility", "id").all().order_by("-id")[:2]
        
        return context
    
    
facility_list_view = FacilityListView.as_view()
    



class FacilityDetailView(View):
    template_name = "facility.html"
    model = Facility
    facility_review_form = FacilityReviewForm
    
    
    def get(self, request, location, category, name, *args, **kwargs):
        facility = get_object_or_404(Facility, location__iexact=location, category__iexact=category, name__iexact=name)
        reviews = Review.objects.filter(facility=facility).all()
        
        context = {"facility":facility,
                   "reviews": reviews,
                   "reviewcount":reviews.count(),
                   "awards": Award.objects.filter(facility=facility).all(),
                   "branches": FacilityBranch.objects.filter(facility=facility).all(),
                   "facilityimages":FacilityImage.objects.filter(name=facility).all(),
                   "branch_pics": Facility.objects.filter(
                       id=facility.pk,
                       facility_pic__name=facility,
                       ).all()[:6],
                   "working_days":WorkingDay.objects.filter(facility=facility).all(),
                   
                   "review_form":self.facility_review_form()
                   }
        
        # print(list(context['branch_pics']))
        return render(request, self.template_name, context)
    
    def post(self, request, location, category, name, *args, **kwargs):
        facility = get_object_or_404(Facility, location__iexact=location, category__iexact=category, name__iexact=name)
        if "reviewform" in request.POST:
            title = request.POST.get("title")
            review = request.POST.get("review")
            if request.user.is_authenticated:
                Review.objects.create(
                facility=facility,
                author=request.user.custom_profile,
                title=title,
                review=review
            )
            else: return redirect(settings.LOGIN_URL)
        return redirect(facility)
        
    
facility_detail_view = FacilityDetailView.as_view()


class DoctorsListView(SpecialityListViewMixin):
    model = User
    template_name = "doctors.html"
    context_object_name = "doctors"
    Type = "DOCTOR"
    count = "doccount"
    


doctors_list_view = DoctorsListView.as_view()




class PharmacyListView(SpecialityListViewMixin):
    model = User
    template_name = "pharmacy.html"
    context_object_name = "pharmacists"
    Type = "PHARMACIST"
    count = "pharmcount"
    
pharmacy_list_view = PharmacyListView.as_view()


class ClinicsListView(ListView):
    model = Facility
    template_name = "clinics.html"
    context_object_name = "clinics"
    
    def get_queryset(self):
        return super().get_queryset().filter(category="CLINIC").all()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cliniccount"] = self.get_queryset().count()
        context['details']="No results found"
        
        
        return context
    
    
clinic_list_view = ClinicsListView.as_view()



class DoctorsDetailView(View):
    model = User
    template_name = "specialist_profile.html"
    review_form_class = ProfileReviewForm
    
    def get(self, request, uid, *args, **kwargs):
        user = get_object_or_404(self.model, custom_profile__uid__iexact=uid)
        owner = get_object_or_404(Profile, user=user)
        
        context = {
            "doctor":user,
            "user":user,
            "facility":Facility.objects.filter(owner=user.custom_profile).all(),
            # "facilityBranches":Facility.objects.get(id=owner.id).facility_branch,
            "feedbackcount":10,
            "accountType":user.type,
            "profile":owner,
            # "name":Profile.objects.get(user=user).unique_id,
            # "full_name":Profile.objects.get(user=user).full_name,
            # "pics": Facility.objects.filter(owner_id=user.custom_profile).all(),
            # "profile_pic":Profile.objects.get(user=user).profile_pic,
            # "services":Profile.objects.get(user=user).services.all()[:3],
            # "pricing":Profile.objects.get(user=user).pricing,
            # "address":Profile.objects.get(user=user).address,
            # "pricing":Profile.objects.get(user=user).pricing
            # acchievements
            # "bio":Profile.objects.get(user=user).bio,
            # "education":Profile.objects.get(user=user).education.all(),
            # "work":Profile.objects.get(user=user).workexpirience.all(),
            # "awards":Profile.objects.get(user=user).award.all(),
            # "specializations":Profile.objects.get(user=user).specializations.all(),
            "reviews_prof":ProfileReview.objects.filter(reviewed=owner).all(),
            
            # forms
            
            "review_form":self.review_form_class()
        }
        
        # print("NAME:", context['hospital'])
        # print(context['pics'])
        return render(request, self.template_name, context)
    
    def post(self, request,uid, *args, **kwargs):
        reviewed = get_object_or_404(self.model, custom_profile__uid__iexact=uid)
        reviewer = self.request.user
        try:
            if "reviewProfile" in request.POST:
                form = self.review_form_class(request.POST)
                context = {}
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.reviewer = reviewer.custom_profile
                    instance.reviewed = reviewed.custom_profile
                    instance.save()
                else:
                    context['form_errors'] = form.errors.as_text()
                    print(context['form_errors'])
                    return render(request, self.template_name, context)
                return render(request, self.template_name, context)
            
        except:
            return redirect(reviewed)


doctor_profile_view = DoctorsDetailView.as_view()
