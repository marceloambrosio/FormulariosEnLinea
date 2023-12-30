from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', HomeView.as_view(), name='home'),
    path('formulario_completado', FormularioCompletadoView.as_view(), name='formulario_completado'),
    path('reempad_comercio_fisica/', ReempadComercioFisicaCreateView.as_view(), name='reempad_comercio_fisica'),
    path('reempad_comercio_fisica_update/<int:pk>/', login_required(ReempadComercioFisicaUpdateView.as_view()), name='reempad_comercio_fisica_update'),
    path('reempad_comercio_fisica_list/', login_required(ReempadComercioFisicaListView.as_view()), name='reempad_comercio_fisica_list'),
    path('reempad_comercio_juridica/', ReempadComercioJuridicaCreateView.as_view(), name='reempad_comercio_juridica'),
    path('reempad_comercio_juridica_update/<int:pk>/', login_required(ReempadComercioJuridicaUpdateView.as_view()), name='reempad_comercio_juridica_update'),
    path('reempad_comercio_juridica_list/', login_required(ReempadComercioJuridicaListView.as_view()), name='reempad_comercio_juridica_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)