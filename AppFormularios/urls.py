from django.urls import path
from django.views.generic.base import RedirectView
from .views import *

urlpatterns = [
    path('reempad_comercio_fisica/', ReempadComercioFisicaCreateView.as_view(), name='reempad_comercio_fisica'),
]