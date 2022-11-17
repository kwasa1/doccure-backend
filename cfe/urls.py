
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from django.conf.urls.static import static
from core import urls as core_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(core_urls, namespace="core")),
    path("account/", include("account.urls", namespace="account")),
    path("auth/", include("authentication.urls", namespace="auth")),
    # path("chats/", include("chats.urls", namespace="chats")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    