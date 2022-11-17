from django.test import TestCase
from django.urls import resolve
from core.views import LandingHomeView


class TestLandingHomeView(TestCase):
    endpoint = "/"
    
    
    def test_root_url_resolve_to_home_view(self):
        root = resolve(self.endpoint)
        
    # def test_user_can_search_facility(self):
    #     pass
        
    
        