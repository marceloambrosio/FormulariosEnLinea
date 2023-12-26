from django.urls import path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('reempad_comercio_fisica/', ReempadComercioFisicaCreateView.as_view(), name='reempad_comercio_fisica'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)