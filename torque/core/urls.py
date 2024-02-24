# Core Django imports
from django.conf.urls import url

# This project apps imports
from . import views

app_name = 'core'
urlpatterns = [
    # ex: /core/about/
    url(r'^about/$', views.about, name='about'),

    # ex: /core/features/
    url(r'^features/$', views.features, name='features'),

    # ex: /core/known_bugs/
    url(r'^known_bugs/$', views.known_bugs, name='known_bugs'),
]
