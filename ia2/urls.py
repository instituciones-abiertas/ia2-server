"""applicationname URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns

from rest_framework_simplejwt import views as jwt_views
import private_storage.urls

from apps.data.routers import get_data_urls
from apps.entity.routers import get_entity_urls

urlpatterns = i18n_patterns(url(r"^$", RedirectView.as_view(url="/admin/")), path("admin/", admin.site.urls)) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

# Private Storage
urlpatterns += [
    url(r"^private/", include(private_storage.urls)),
]

# Router patterns
urlpatterns = urlpatterns + [
    url(r"^api/", include(get_entity_urls())),
    url(r"^api/stats/", include(get_data_urls())),
]

# Auth patterns
urlpatterns = urlpatterns + [
    path("api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    from django.views.defaults import page_not_found

    urlpatterns += i18n_patterns(
        url(r"^404/$", page_not_found),
    )

# Only enable debug toolbar if it's an installed app
if apps.is_installed("debug_toolbar"):
    import debug_toolbar

    urlpatterns += [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ]
