def make_verified_facility(self, request, queryset):
    queryset.update(is_verified=True)
    
make_verified_facility.shortdescription = "Verify Facility"