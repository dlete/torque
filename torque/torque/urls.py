"""torque URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

# Core Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

# Third-party app imports
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Torque API')


urlpatterns = [
    # Django built-in admin site
    path('admin/', admin.site.urls),

    # Django REST Framework, http://www.django-rest-framework.org/
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Django REST Swagger, https://django-rest-swagger.readthedocs.io/en/latest/
    url(r'^api-doc/', schema_view),

    # This project apps
    path('audits/', include('audits.urls')),
    path('api/v1/', include('apiv1.urls')),
    path('core/', include('core.urls')),
    path('catalogues/', include('catalogues.urls')),
    path('inventories/', include('inventories.urls')),
]


# Use static() to add url mapping to serve static files during development (only)
# https://docs.djangoproject.com/en/2.0/howto/static-files/#serving-static-files-during-development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# This is the landing page. Redirects the base URL '/' (or empty) to '/inventories/'.
# Taken from https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/skeleton_website
# Leave the first parameter of the path function empty to imply '/'.
# If you write the first parameter as '/' Django will give you the following warning:
# ?: (urls.W002) Your URL pattern '/' has a route beginning with a '/'.
# Remove this slash as it is unnecessary.
from django.views.generic.base import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/inventories/', permanent=True)),
]
