from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import ReempadComercioFisica, ReempadComercioJuridica
from .forms import ReempadComercioFisicaForm, ReempadComercioJuridicaForm

# Create your views here.

class ReempadComercioFisicaCreateView(CreateView):
    model = ReempadComercioFisica
    form_class = ReempadComercioFisicaForm
    template_name = 'reempad_comercio_fisica.html'
    success_url = reverse_lazy('home')

class ReempadComercioJuridicaCreateView(CreateView):
    model = ReempadComercioJuridica
    form_class = ReempadComercioJuridicaForm
    template_name = 'reempad_comercio_juridica.html'
    success_url = reverse_lazy('home')