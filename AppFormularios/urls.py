from django.urls import path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('reempad_comercio_fisica/', ReempadComercioFisicaCreateView.as_view(), name='reempad_comercio_fisica'),
    path('reempad_comercio_fisica_update/<int:pk>/', ReempadComercioFisicaUpdateView.as_view(), name='reempad_comercio_fisica_update'),
    path('reempad_comercio_fisica_list/', ReempadComercioFisicaListView.as_view(), name='reempad_comercio_fisica_list'),
    path('reempad_comercio_juridica/', ReempadComercioJuridicaCreateView.as_view(), name='reempad_comercio_juridica'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)