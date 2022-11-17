
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Facility

@register(Facility)
class FacilityModelIndex(AlgoliaIndex):
    fields = (
    "owner","name","location","core_services","category","services","is_verified","address",
    )
    # geo_field = 'location'
    # settings = {'searchableAttributes': ['name',"location","services",'address']}
    index_name = 'cfe_facility_index'