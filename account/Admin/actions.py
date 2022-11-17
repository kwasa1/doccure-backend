# custom actions

def make_subscribed(self, request, queryset):
    queryset.update(is_subscribed=True)
    
make_subscribed.shortdescription="Make Subscribed"

def verify_health_workers(modelname, queryset, request):
    queryset.update(is_verified=True)
    
verify_health_workers.shortdescription = "Verify Professionals"